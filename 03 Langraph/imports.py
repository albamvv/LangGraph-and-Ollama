from typing import Annotated, TypedDict
from datetime import datetime
from dotenv import load_dotenv  # Used to load environment variables from a .env file
from langchain_ollama import ChatOllama  # LangChain integration for Ollama models
import os  # Provides functions to interact with the operating system
from langgraph.graph import StateGraph, START, END  # StateGraph is used to build a structured conversation flow
from langgraph.graph.message import add_messages 
from IPython.display import display, Image # Import IPython utilities to visualize the 
from langchain_community.tools.tavily_search import TavilySearchResults  # Web search tool 
from langchain_community.tools import TavilySearchResults
from langgraph.prebuilt import ToolNode, tools_condition  # Prebuilt components for LangGraph   
from langchain_core.messages import HumanMessage  # Handles message exchange in LangChain  
from langchain_core.tools import tool  # Decorator to define tools  
from langgraph.checkpoint.memory import MemorySaver # Import memory management for saving conversation state  

