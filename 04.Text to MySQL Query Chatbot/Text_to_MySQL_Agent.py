from langgraph.graph import  START, StateGraph
from IPython.display import display, Image
from query_utils import write_query,execute_query, generate_answer,save_and_open_graph
from config import State

# Ask how many employees are in the database
question = "how many employees are there?"
#question = "List all the albums"
query = write_query({"question": question})
print("query-> ",query)

# Execute the generated query
result = execute_query(query)
print("result-> ",result)

# Combine all information into a state dictionary
state_dict= {"question": question, **query, **result}
print("state ->",state_dict)

# Generate and print the final answer
print("answer-> ",generate_answer(state_dict))

# ------------ Building the graph ---------------

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
save_and_open_graph(graph, filename="custom_graph.png") # Save and open the graph image

