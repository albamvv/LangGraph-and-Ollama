from imports import *
from utils import save_and_open_graph

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

# Initialize the ChatOllama model with the specified configuration
llm = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")
response = llm.invoke("tell me something about the sea in 5 lines")

# Define the state structure for the chatbot. State contains a list of messages, processed using add_messages
class State(TypedDict):
    #{"message":"your message"}
    messages: Annotated[list, add_messages]
 
# Define the chatbot function, which takes the current state and generates a response
def chatbot(state: State):
    response = llm.invoke(state["messages"])  # Invoke the LLM with the current messages
    return {"messages": [response]}  # Return the response as part of the state

# Create a state graph to manage the chatbot's flow
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)# Add a chatbot node to handle messages
# Define edges (transitions) between different states # START --> chatbot --> END
graph_builder.add_edge(START, "chatbot")  # Start the conversation with the chatbot
graph_builder.add_edge("chatbot", END)  # End conversation after the chatbot responds
graph = graph_builder.compile() # Compile the graph

# Save and open the graph image
save_and_open_graph(graph)

# Invoke the graph with initial messages
graph.invoke({"messages": ["Hi", "myself is Laxmi Kant"]})
# response is a dictionary with a 'messages' key that contains a list of HumanMessage and AIMessage objects.
response=graph.invoke({"messages": ["tell me something about the sea in ten words"]})
print("response-> ",response)

# Extraer la respuesta del asistente
ai_response = response["messages"][-1].content 
#print("AI response-> ",ai_response)  # Imprime solo el texto de la respuesta

'''
# Continuous chat loop for user interaction
while True:
    user_input = input("You: ")  # Get user input
    if user_input in ['q', 'quit', 'exit']:  # Exit condition
        print("Bye!")
        break
    
    response = graph.invoke({"messages": [user_input]})  # Process user input through the graph
    print("Assistant:", response["messages"][-1].content)  # Print the chatbot's response

'''