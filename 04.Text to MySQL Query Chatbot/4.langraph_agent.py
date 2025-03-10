from config import prompt,db, llm
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from query_utils import save_and_open_graph
from langchain_community.tools import QuerySQLDatabaseTool

# LangGraph AGENTS: Automating query execution with AI
'''
# Agents can:
# - Query the database multiple times to refine their answer.
# - Recover from errors by detecting failed queries and regenerating them.
# - Answer questions based on both schema structure and database content.
'''

#prompt.messages[0].pretty_print()

system_prompt = prompt.invoke({'dialect': db.dialect, 'top_k': 5}).to_string()
system_prompt = prompt.format(dialect = db.dialect, top_k = 5)

# Create an instance of SQLDatabaseToolkit, which is a LangChain tool used to interact with SQL databases through a language model (LLM).
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
#toolkit = QuerySQLDataBaseTool(db=db, llm=llm)
#print("toolkit context-> ",toolkit.get_context())

# Retrieve available tools from the toolkit
tools = toolkit.get_tools()
#print("tools-> ", tools)  # Print the list of available tools

# Invoke the first tool to execute an SQL query selecting two rows from the "Album" table
#print(tools[0].invoke("select * from Album LIMIT 2"))
#print(tools[1].invoke("Album,Customer"))

##----------------------- Agent coding ------------------------------------
# Create an agent using a ReAct (Reasoning + Acting) framework, providing the language model (llm), available tools, and a system prompt to modify its state.
agent_executor = create_react_agent(llm, tools, state_modifier=system_prompt)
#save_and_open_graph(agent_executor, filename="assets/agent_graph.png") # Save and open the graph image


#----------------- Define a question to analyze customer purchases by country
question = "Which country's customers have made the most purchases?"
query = {"messages": [HumanMessage(question)]}

# Stream the agent's responses step by step while processing the query
for step in agent_executor.stream(query, stream_mode="updates"):
    #print("step-> ",step)  # Print each step of the execution
    print("--------------------------------")
    # The following line is commented out; it likely formats and prints the last message in the response
    #step['messages'][-1].pretty_print()
    if 'agent' in step and 'messages' in step['agent']:
        ultimo_mensaje = step['agent']['messages'][-1]  # Último mensaje del agente
        print("Mensaje del agente:", ultimo_mensaje.content)

    elif 'tools' in step and 'messages' in step['tools']:
        ultimo_mensaje = step['tools']['messages'][-1]  # Último mensaje de herramientas
        print("Mensaje de herramienta:", ultimo_mensaje.content)

    else:
        print("No se encontró un mensaje válido en step:", step)




