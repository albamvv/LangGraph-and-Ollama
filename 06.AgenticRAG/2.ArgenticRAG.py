from imports import*
from config import llm, embeddings,db_name, State,retriever_tool
from utils import grade_documents, agent,rewrite, generate, save_and_open_graph


# -------------------- Graph ------------------------

graph_builder = StateGraph(State)
graph_builder.add_node("agent", agent)
retriever = ToolNode([retriever_tool])
graph_builder.add_node("retriever", retriever)
graph_builder.add_node("rewrite", rewrite)
graph_builder.add_node("generate", generate)
graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges( 
    "agent",
    tools_condition,
    {
        "tools": "retriever",
        END: END
    }
)

graph_builder.add_conditional_edges(
    "retriever",
    grade_documents
)

graph_builder.add_edge("generate", END)
graph_builder.add_edge("rewrite", "agent")
graph = graph_builder.compile()
#save_and_open_graph(graph, filename="assets/agent_tool_graph.png") # Save and open the graph image

#------------------- Example ---------------

# query = {"messages": [HumanMessage("How to gain muscle mass?")]}
query = {"messages": [HumanMessage("what are the risks of taking too much protein?")]}
# query = {"messages": [HumanMessage("tell me about the langchain")]}

# graph.invoke(query)

for output in graph.stream(query):
    for key, value in output.items():
        pprint(f"Output from node '{key}':")
        pprint("----")
        pprint(value, indent=4, width=120)

    pprint("\n------\n")
