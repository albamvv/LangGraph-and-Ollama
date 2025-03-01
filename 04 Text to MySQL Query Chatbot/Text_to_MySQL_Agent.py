from dotenv import load_dotenv
import os
import requests
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_ollama import ChatOllama
from typing import  TypedDict, Annotated
from langgraph.graph import  START, StateGraph
from IPython.display import display, Image
from langchain import hub


load_dotenv('../.env')

# Download the Chinook database
url = "https://github.com/laxmimerit/All-CSV-ML-Data-Files-Download/raw/refs/heads/master/db_samples/Chinook.db"

response = requests.get(url)

if response.status_code == 200:
    with open("Chinook.db", "wb") as file:
        file.write(response.content)
    print("File downloaded successfully")
else:
    print("Failed to download the file")
    print(response.status_code)

# LLM Connection and MySQL Tools

db = SQLDatabase.from_uri("sqlite:///Chinook.db")
db.dialect

print(db.get_usable_table_names())
#['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice', 'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track']
db.run("SELECT * FROM album LIMIT 2")

db.run("SELECT * FROM artist LIMIT 2")
#"[(1, 'AC/DC'), (2, 'Accept')]"
db.run("select * from Invoice as inv join Customer as c on inv.CustomerId=c.CustomerId LIMIT 1")

#LLM Connection

model = "qwen2.5" # llama3.2:3b
llm = ChatOllama(model=model, base_url = "http://localhost:11434")
llm.invoke("Hello")

#Application State or Graph State

class State(TypedDict):
    question: str # user question
    query: str # mysql query prepared by llm
    result: str # mysql result
    answer: str # llm answer
from langchain import hub

query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
query_prompt_template.messages[0].pretty_print()

#Write, Execute and Generate MySQL Response
#Write Node for MySQL Query
class QueryOutput(TypedDict):
    """Generated SQL query"""

    query: Annotated[str, ..., "Syntactically correct and valid SQL query"]

QueryOutput({"query": "SELECT * FROM album LIMIT 2"})
QueryOutput.__annotations__

# print(db.get_table_info())
llm.with_structured_output(QueryOutput)

def write_query(state:State):
    """Generate MySQL query to fetch information"""
    prompt = query_prompt_template.invoke({
        "dialect": db.dialect,
        "top_k": 5,
        "table_info": db.get_table_info(),
        "input": state["question"]
    })

    structured_llm = llm.with_structured_output(QueryOutput)

    result = structured_llm.invoke(prompt)

    return {"query": result["query"]}

write_query({"question": "List all the albums"})
#{'query': 'SELECT AlbumId, Title FROM Album'}
query_prompt_template

write_query({"question": "How many employees are there?"})
#{'query': 'SELECT COUNT(*) AS EmployeeCount FROM Employee'}

#Execute Query
db.run('SELECT COUNT(*) AS EmployeeCount FROM Employee')
db.run('SELECT AlbumId, Title FROM Album')



def execute_query(state:State):
    """Execute SQL query and return the result"""
    query = state["query"]
    execute_query_tool = QuerySQLDataBaseTool(db=db)

    return {'result': execute_query_tool.invoke({"query": query})}

execute_query({"query": "SELECT * FROM album LIMIT 2"})

#Generate Answer
# question, query, result, answer
def generate_answer(state:State):
    """Generate answer using retrieved information as the context""" 

    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )

    response = llm.invoke(prompt)

    return {"answer": response.content}
question = "how many employees are there?"
query = write_query({"question": question})
print(query)
#{'query': 'SELECT COUNT(*) AS NumberOfEmployees FROM Employee;'}
result = execute_query(query)
print(result)
#{'result': '[(8,)]'}
state = {"question": question, **query, **result}
print(state)
'''
{'question': 'how many employees are there?',
 'query': 'SELECT COUNT(*) AS NumberOfEmployees FROM Employee;',
 'result': '[(8,)]'}
 '''
print(generate_answer(state))
#{'answer': 'Based on the provided SQL query and result, there are 8 employees in total. The `COUNT(*)` function returned the number of rows in the `Employee` table, which corresponds to the number of employees.'}

#Building Graph

graph_builder = StateGraph(State)

graph_builder.add_node("write_query", write_query)
graph_builder.add_node("execute_query", execute_query)
graph_builder.add_node("generate_answer", generate_answer)

graph_builder.add_edge(START, "write_query")
graph_builder.add_edge("write_query", "execute_query")
graph_builder.add_edge("execute_query", "generate_answer")

graph = graph_builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))

query = {'question': 'List all the albums'}
for step in graph.stream(query, stream_mode="updates"):
    print(step)

# query = {'question': 'Hello'}
# for step in graph.stream(query, stream_mode="updates"):
#     print(step)

# LangGraph AGENTS
'''
They can query the database as many times as needed to answer the user question.
They can recover from errors by running a generated query, catching the traceback and regenerating it correctly.
They can answer questions based on the databases' schema as well as on the databases' content (like describing a specific table).
'''

prompt = hub.pull("langchain-ai/sql-agent-system-prompt")
prompt.messages[0].pretty_print()