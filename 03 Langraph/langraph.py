# Import necessary libraries
from dotenv import load_dotenv  # Used to load environment variables from a .env file
from langchain_ollama import ChatOllama  # LangChain integration for Ollama models
import os  # Provides functions to interact with the operating system

from typing import Annotated, TypedDict 
from langgraph.graph import StateGraph, START, END  # StateGraph is used to build a structured conversation flow
from langgraph.graph.message import add_messages 
from langchain_ollama import ChatOllama
from IPython.display import display, Image # Import IPython utilities to visualize the graph

'''
This Python script sets up a chatbot using LangChain and the Ollama model. 
It loads environment variables, initializes a language model (llama3.2:3b), and defines a chatbot function that processes user messages. 
A state graph is built using StateGraph to manage conversation flow. The chatbot receives input, generates responses, 
and maintains conversation history. The graph structure is visualized using IPython. 
The script includes a loop for continuous user interaction, allowing users to chat with the bot until they exit by typing 'q', 'quit', or 'exit'.
https://langchain-ai.github.io/langgraph/reference/graphs/
https://python.langchain.com/docs/tutorials/llm_chain/ 
'''

# Load environment variables from the .env file
load_dotenv()

# Retrieve environment variables (not used in this script)
api_key = os.getenv("LANGCHAIN_API_KEY")  # API key for LangChain (if needed)
endpoint = os.getenv("LANGCHAIN_ENDPOINT")  # Endpoint URL for LangChain API (if needed)
tracing = os.getenv("LANGSMITH_TRACING")  # Tracing option for debugging (if needed)

# Debugging: Print the retrieved environment variables (commented out)
# print(f"API Key: {api_key}")
# print(f"Endpoint: {endpoint}")
# print(f"Tracing: {tracing}")


# Initialize the ChatOllama model with the specified configuration
llm = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")
#print("llm-> ",llm)
# Test the model with a simple greeting message
response = llm.invoke("tell me something about the sea in 5 lines")
#print('response-> ', response.content)


'''
State is a TypedDict that defines a chatbot's state.
messages is a list processed using add_messages
Annotated[list, add_messages] is a hint that messages should be modified by add_messages.
'''
# Define the state structure for the chatbot
class State(TypedDict):
    # State contains a list of messages, processed using add_messages
    messages: Annotated[list, add_messages]

'''
# Define the chatbot function, which takes the current state and generates a response
def chatbot(state: State):
    response = llm.invoke(state["messages"])  # Invoke the LLM with the current messages
    return {"messages": [response]}  # Return the response as part of the state


# Create a state graph to manage the chatbot's flow
graph_builder = StateGraph(State)
# Add a chatbot node to handle messages
graph_builder.add_node("chatbot", chatbot)

# Define edges (transitions) between different states
graph_builder.add_edge(START, "chatbot")  # Start the conversation with the chatbot
graph_builder.add_edge("chatbot", END)  # End conversation after the chatbot responds

# Compile the graph
graph = graph_builder.compile()

# Display the graph structure as an image
display(Image(graph.get_graph().draw_mermaid_png()))

# Invoke the graph with initial messages
graph.invoke({"messages": ["Hi", "myself is Laxmi Kant"]})
graph.invoke({"messages": ["Hello"]})


# Continuous chat loop for user interaction
while True:
    user_input = input("You: ")  # Get user input
    if user_input in ['q', 'quit', 'exit']:  # Exit condition
        print("Bye!")
        break
    
    response = graph.invoke({"messages": [user_input]})  # Process user input through the graph
    print("Assistant:", response["messages"][-1].content)  # Print the chatbot's response

'''