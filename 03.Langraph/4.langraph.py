from imports import *
from utils import save_and_open_graph, State, llm, tools, llm_with_tools,chatbot

'''
This repository contains a Python script that implements a chatbot using LangChain, LangGraph, and the Ollama (llama3.2:3b) model.  
The chatbot manages conversations using a state graph and allows continuous interaction with the user.
'''
# Load environment variables from the .env file
load_dotenv()

# Retrieve environment variables (not used in this script)
api_key = os.getenv("LANGCHAIN_API_KEY")  # API key for LangChain (if needed)
endpoint = os.getenv("LANGCHAIN_ENDPOINT")  # Endpoint URL for LangChain API (if needed)
tracing = os.getenv("LANGSMITH_TRACING")  # Tracing option for debugging (if needed)

# Create a state graph to manage the chatbot's flow
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)# Add a chatbot node to handle messages
# Define edges (transitions) between different states # START --> chatbot --> END
graph_builder.add_edge(START, "chatbot")  # Start the conversation with the chatbot
graph_builder.add_edge("chatbot", END)  # End conversation after the chatbot responds
graph = graph_builder.compile() # Compile the graph
save_and_open_graph(graph)# Save and open the graph image

# Invoke the graph with initial messages. Response is a dictionary with a 'messages' key that contains a list of HumanMessage and AIMessage objects.
response=graph.invoke({"messages": ["tell me something about the sea in ten words"]})
ai_response = response["messages"][-1].content  # Extraer la respuesta del asistente
#print("AI response-> ",ai_response)  # Imprime solo el texto de la respuesta

# Continuous chat loop for user interaction
while True:
    user_input = input("You: ")  # Get user input
    if user_input in ['q', 'quit', 'exit']:  # Exit condition
        print("Bye!")
        break   
    response = graph.invoke({"messages": [user_input]})  # Process user input through the graph
    print("Assistant:", response["messages"][-1].content)  # Print the chatbot's response

