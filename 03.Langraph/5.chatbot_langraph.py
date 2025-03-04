from imports import *
from utils import internet_search,llm_search,save_and_open_graph  # Import the externalized function

'''
This script sets up a chatbot using LangGraph, LangChain, and Ollama (a local LLM). 
The chatbot is capable of answering user queries either by using an LLM or by searching the web for real-time information.
'''

# Initialize the LLM using the LLaMA 3.2 model, hosted locally  
llm = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")

tools = [internet_search, llm_search] # Lista de herramientas disponibles 
llm_with_tools = llm.bind_tools(tools) # Bind the tools to the LLM, allowing it to decide when to use them 

# Define the state structure for the chatbot
class State(TypedDict):
    messages: Annotated[list, add_messages]
 
# Define the chatbot function, which takes the current state and generates a response
def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])  # Invoke the LLM with the current messages
    return {"messages": [response]}  # Return the response as part of the state

memory = MemorySaver()  # Initialize memory for tracking conversations  

# Create a LangGraph state machine for managing chatbot interactions  
graph_builder = StateGraph(State)  
graph_builder.add_node("chatbot", chatbot)  # Add chatbot processing node  
tool_node = ToolNode(tools=tools)# Create a node for handling external tools (LLM and web search)  
graph_builder.add_node("tools", tool_node)  
graph_builder.add_conditional_edges("chatbot", tools_condition) # Define conditions for switching between chatbot and tools  
graph_builder.add_edge("tools", "chatbot")  # Set up the interaction flow between nodes  
graph_builder.set_entry_point("chatbot")  # Define the starting point  
#graph = graph_builder.compile()
graph = graph_builder.compile(checkpointer=memory)  # Compile the graph and enable memory tracking  
save_and_open_graph(graph)# Save and open the graph image


# Example: Query the chatbot about Earth  
config = {"configurable": {"thread_id": 1}}  
output = graph.invoke({"messages": ["Tell me about the earth in 3 points"]}, config=config)  
#print("output-> ",output)
tool_message = output["messages"][2]  # Accede directamente
#print(tool_message.content)  # Ver el contenido

# Start an interactive chatbot loop  
while True:
    user_input = input()  # Wait for user input  
    if user_input in ["exit", "quit", "q"]:  # Exit conditions  
        print("Exiting...")  
        break  

    output = graph.invoke({"messages": [user_input]}, config=config)  # Get chatbot response  
    print(output)  # Display the response  


