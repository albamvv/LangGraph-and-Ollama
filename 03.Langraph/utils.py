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
