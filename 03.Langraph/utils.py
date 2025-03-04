from imports import *

def save_and_open_graph(graph, filename="langraph_flow.png"):
    """
    Saves the graph structure as a PNG file and opens it automatically.
    
    Parameters:
    - graph: The LangGraph graph object.
    - filename: The name of the output image file (default: "langraph_flow.png").
    """
    image_bytes = graph.get_graph().draw_mermaid_png()
    
    # Save the image as a PNG file
    with open(filename, "wb") as f:
        f.write(image_bytes)
    
    # Open the image file (compatible with Windows, macOS, and Linux)
    #os.system(filename)


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

