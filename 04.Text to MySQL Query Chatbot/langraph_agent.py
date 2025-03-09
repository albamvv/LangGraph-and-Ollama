from config import prompt,db, llm
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

# LangGraph AGENTS: Automating query execution with AI
'''
# Agents can:
# - Query the database multiple times to refine their answer.
# - Recover from errors by detecting failed queries and regenerating them.
# - Answer questions based on both schema structure and database content.
'''

#prompt.messages[0].pretty_print()

system_prompt = prompt.invoke({'dialect': db.dialect, 'top_k': 5})
#print("system_prompt-> ",system_prompt)
#system_prompt = prompt.format(dialect = db.dialect, top_k = 5)

# Create an instance of SQLDatabaseToolkit, which is a LangChain tool used to interact with SQL databases through a language model (LLM).
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
print("toolkit context-> ",toolkit.get_context())

'''
tools = toolkit.get_tools()
print("tools-> ",tools)

tools[0].invoke("select * from Album LIMIT 2")
# print(tools[1].invoke("Album,Customer"))

agent_executor = create_react_agent(llm, tools, state_modifier=system_prompt)

display(Image(agent_executor.get_graph().draw_mermaid_png()))

question = "Which country's customers have made the most purchases?"
query = {"messages": [HumanMessage(question)]}

for step in agent_executor.stream(query, stream_mode="updates"):
    print(step)
    # step['messages'][-1].pretty_print()

'''


