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


# Build the processing graph
graph_builder = StateGraph(State)
graph_builder.add_node("write_query", write_query)
graph_builder.add_node("execute_query", execute_query)
graph_builder.add_node("generate_answer", generate_answer)

# Define the execution flow of the graph
graph_builder.add_edge(START, "write_query")
graph_builder.add_edge("write_query", "execute_query")
graph_builder.add_edge("execute_query", "generate_answer")

# Compile and visualize the graph
graph = graph_builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))

# Example: Query to list all albums
query = {'question': 'List all the albums'}
for step in graph.stream(query, stream_mode="updates"):
    print(step)

# LangGraph AGENTS: Automating query execution with AI
'''
# Agents can:
# - Query the database multiple times to refine their answer.
# - Recover from errors by detecting failed queries and regenerating them.
# - Answer questions based on both schema structure and database content.
'''

prompt = hub.pull("langchain-ai/sql-agent-system-prompt")
prompt.messages[0].pretty_print()
