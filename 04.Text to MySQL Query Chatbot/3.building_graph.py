from query_utils import write_query,execute_query, generate_answer,save_and_open_graph
from langgraph.graph import  START, StateGraph
from config import State

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
#save_and_open_graph(graph, filename="building_graph.png") # Save and open the graph image

# Example: Query to list all albums
query = {'question': 'List all the albums'}
for step in graph.stream(query, stream_mode="updates"):
    print(step)

