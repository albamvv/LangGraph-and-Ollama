from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from config import State, llm, db,query_prompt_template,QueryOutput

# NODE -> WRITE QUERY

# Function to generate an SQL query from a user's question
def write_query(state: State):
    """Generate an SQL query to fetch information based on the user's question"""
    prompt = query_prompt_template.invoke({
        "dialect": db.dialect,
        "top_k": 5,
        "table_info": db.get_table_info(),
        "input": state["question"]
    })

    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)

    return {"query": result["query"]}


#print("promtp template -> ",query_prompt_template)
response_query=write_query({"question":"List all the albums"})
#print("response query-> ",response)
# response query->  {'query': 'SELECT * FROM Album'}


# Function to execute a given SQL query and return results
def execute_query(state: State):
    """Execute an SQL query and return the result"""
    query = state["query"]
    execute_query_tool = QuerySQLDataBaseTool(db=db)

    return {"result": execute_query_tool.invoke({"query": query})}
result_query=execute_query(response_query)

# Function to generate a response based on SQL query results
def generate_answer(state: State):
    """Generate an answer using retrieved information from the database"""
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )

    response = llm.invoke(prompt)

    return {"answer": response.content}


def save_and_open_graph(graph, filename="langraph_flow.png"):
    """
    Saves the graph structure as a PNG file and opens it automatically.
    
    Parameters:
    - graph: The LangGraph graph object.
    - filename: The name of the output image file (default: "langraph_flow.png").
    """
    image_bytes = graph.get_graph().draw_mermaid_png()
    
    # Guardar la imagen con el nombre especificado
    with open(filename, "wb") as f:
        f.write(image_bytes)

    # Open the image file (compatible with Windows, macOS, and Linux)
    #os.system(filename)
    print(f"Graph saved as {filename}")


