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
from langchain.schema import AIMessage


# Load environment variables from a .env file
load_dotenv('../.env')

##------------------------ LLM connection and MySQL Tools ---------------------------------
# Initialize SQL Database connection
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
print("Chinok db->",db)
print("Dialect->", db.dialect)
# Print available table names in the database
print("Tables names-> ",db.get_usable_table_names())

# Execute some test queries to inspect the database content
print("Album-> ",db.run("SELECT * FROM album LIMIT 2")) # AlbumId, Title, ArtistId
print("Artist-> ",db.run("SELECT * FROM artist LIMIT 2")) #ArtistId, Name
print(db.run("SELECT * FROM Invoice AS inv JOIN Customer AS c ON inv.CustomerId=c.CustomerId LIMIT 1"))

# Set up a connection to the LLM (Ollama model)
model = "qwen2.5"  # Alternative model: llama3.2:3b
llm = ChatOllama(model=model, base_url="http://localhost:11434")
response=llm.invoke("Hello")
print("response-> ",response)
ai_message = AIMessage(content=response.content)
print("AIMessage-> ",ai_message)
#--------------------- Aplication State ----------------------