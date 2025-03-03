# Importing necessary components from LangChain and LangGraph  
from langchain_community.tools.tavily_search import TavilySearchResults  # Web search tool 
from langchain_community.tools import TavilySearchResults
from langgraph.prebuilt import ToolNode, tools_condition  # Prebuilt components for LangGraph  
from typing import Annotated, TypedDict 
from langchain_core.messages import HumanMessage  # Handles message exchange in LangChain  
from langchain_core.tools import tool  # Decorator to define tools  
from langchain_ollama import ChatOllama  # Interface for using the Ollama LLM  
from langgraph.checkpoint.memory import MemorySaver # Import memory management for saving conversation state  
from langgraph.graph.message import add_messages 
from langgraph.graph import StateGraph
import os  # Provides functions to interact with the operating system
'''
This script sets up a chatbot using LangGraph, LangChain, and Ollama (a local LLM). 
The chatbot is capable of answering user queries either by using an LLM or by searching the web for real-time information.
'''

# Initialize the LLM using the LLaMA 3.2 model, hosted locally  
llm = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")
#print(llm.invoke("hi"))


@tool
def internet_search(query: str):
    """
    Search the web for real-time and latest information.
    This is useful for getting news updates, stock market trends, weather forecasts, etc.
    Args:
        query (str): The search query.
    Returns:
        response (dict): Search results retrieved from the web.
    """
    search = TavilySearchResults(
        max_results=3,  # Limit the number of search results  
        search_depth='advanced',  # Perform an in-depth search  
        include_answer=True,  # Include a concise answer in the response  
        include_raw_content=True,  # Retrieve raw content from search results  
    )
    response = search.invoke(query)  # Execute the search query  
    return response


@tool
def llm_search(query: str):
    """
    Use the LLM model for general and basic information.
    Args:
        query (str): The user’s question.
    Returns:
        response (str): LLM-generated response.
    """
    response = llm.invoke(query)  # Query the local LLaMA 3.2 model  
    return response

# Define a list of available tools (LLM and web search)  
tools = [internet_search, llm_search]

# Bind the tools to the LLM, allowing it to decide when to use them  
llm_with_tools = llm.bind_tools(tools)

# Define the state structure for the chatbot
class State(TypedDict):
    messages: Annotated[list, add_messages]
 
# Define the chatbot function, which takes the current state and generates a response
def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])  # Invoke the LLM with the current messages
    return {"messages": [response]}  # Return the response as part of the state

# Create a LangGraph state machine for managing chatbot interactions  
graph_builder = StateGraph(State)  
# Add chatbot processing node  
graph_builder.add_node("chatbot", chatbot)  
# Create a node for handling external tools (LLM and web search)  
tool_node = ToolNode(tools=tools)  
graph_builder.add_node("tools", tool_node)  

# Define conditions for switching between chatbot and tools  
graph_builder.add_conditional_edges("chatbot", tools_condition) 

# Set up the interaction flow between nodes  
graph_builder.add_edge("tools", "chatbot")  
graph_builder.set_entry_point("chatbot")  # Define the starting point  

memory = MemorySaver()  # Initialize memory for tracking conversations  
# Compile the graph and enable memory tracking  
graph = graph_builder.compile()
#graph = graph_builder.compile(checkpointer=memory)  

# Display a graphical representation of the chatbot’s workflow  
image_bytes = graph.get_graph().draw_mermaid_png()
with open("chatbot_langraph_flow.png", "wb") as f:
    f.write(image_bytes)
os.system("chatbot_langraph_flow.png")  # En Windows


''' 
# Example: Query the chatbot about Earth  
config = {"configurable": {"thread_id": 1}}  
output = graph.invoke({"messages": ["Tell me about the earth in 3 points"]}, config=config)  
output  

# Start an interactive chatbot loop  
while True:
    user_input = input()  # Wait for user input  
    if user_input in ["exit", "quit", "q"]:  # Exit conditions  
        print("Exiting...")  
        break  

    output = graph.invoke({"messages": [user_input]}, config=config)  # Get chatbot response  
    print(output)  # Display the response  

    '''
