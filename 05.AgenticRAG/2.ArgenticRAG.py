from imports import*
from config import llm, embeddings,db_name, State
from utils import grade_documents, agent,rewrite, generate, save_and_open_graph
# -------------------- Retriever ------------------------

vector_store = FAISS.load_local(db_name, embeddings, allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs = {'k': 5})
question = "how to gain muscle mass?"
response=retriever.invoke(question)
'''
for doc in response:
    print(f"📄 Source: {doc.metadata['source']} (Page {doc.metadata['page']})")
    print(f"📌 Content: {doc.page_content}\n")

'''

retriever_tool = create_retriever_tool(
    retriever,
    "health_supplements", # tool name
    "Search and return information about the Health Supplements for workout and gym",
)

tools = [retriever_tool]
#print("tools-> ",tools)

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
save_and_open_graph(graph, filename="assets/agent_tool_graph.png") # Save and open the graph image
