from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


llm = ChatOllama(model="llama3.2:3b", base_url = "http://localhost:11434")

@tool
def internet_search(query: str):
    """
    Search the web for realtime and latest information.
    for examples, news, stock market, weather updates etc.
    
    Args:
    query: The search query
    """
    search = TavilySearchResults(
        max_results=3,
        search_depth='advanced',
        include_answer=True,
        include_raw_content=True,
    )

    response = search.invoke(query)

    return response

@tool
def llm_search(query: str):
    """
    Use the LLM model for general and basic information.
    """
    response = llm.invoke(query)
    return response

tools = [internet_search, llm_search]
tools

llm_with_tools = llm.bind_tools(tools)
llm_with_tools

class State(TypedDict):
    # {"messages": ["your message"]}
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges("chatbot", tools_condition)

graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")

graph = graph_builder.compile(checkpointer=memory)

display(Image(graph.get_graph().draw_mermaid_png()))


# graph.invoke({"messages": ["Tell me about the earth in 3 points"]})

config = {"configurable": {"thread_id": 1}}
output = graph.invoke({"messages": ["Tell me about the earth in 3 points"]}, config=config)
output

config = {"configurable": {"thread_id": 1}}

while True:
    user_input = input()
    if user_input in ["exit", "quit", "q"]:
        print("Exiting...")
        break

    output = graph.invoke({"messages": [user_input]}, config=config)
    # output['messages'][-1].pretty_print()
    print(output)