from imports import*
from config import llm,tools


# ----------------------- LOAD PDFs -------------------------------

def load_pdfs_from_directory(directory_path):
    """
    Loads all PDFs from the specified directory and its subdirectories.

    Args:
        directory_path (str): The root directory to search for PDFs.

    Returns:
        list: A list of documents loaded from the PDFs.
    """
    # List to store the paths of all PDF files
    pdfs = []
    # os.walk() iterates through all directories and files inside "rag-dataset"
    # root -> The current folder being scanned  
    # dirs -> List of subdirectories in the current folder  
    # files -> List of files in the current folder  

    # Walk through the directory and find all PDF files
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".pdf"):
                pdfs.append(os.path.join(root, file))

    # List to store the loaded documents
    docs = []

    # Load documents from each PDF
    for pdf in pdfs:
        loader = PyMuPDFLoader(pdf)
        temp = loader.load()
        docs.extend(temp)

    return docs


# ---------------------- Document grader ---------------------------

def grade_documents(state) -> Literal["generate", "rewrite"]:
    """
    Determines whether the retrieved documents are relevant to the question.
    Args:
        state (messages): The current state
    Returns:
        str: A decision for whether the documents are relevant or not
    """

    print("---CHECK RELEVANCE---")

    # Data model
    class grade(BaseModel):
        """Binary score for relevance check."""

        binary_score: str = Field(description="Relevance score 'yes' or 'no'")

    # LLM with tool and validation
    llm_with_structured_output = llm.with_structured_output(grade)

    # Prompt
    prompt = PromptTemplate(
        template="""You are a grader assessing relevance of a retrieved document to a user question. \n 
        Here is the retrieved document: \n\n {context} \n\n
        Here is the user question: {question} \n
        If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
        input_variables=["context", "question"],
    )

    # Chain
    chain = prompt | llm_with_structured_output

    messages = state["messages"]
    last_message = messages[-1]

    question = messages[0].content
    docs = last_message.content

    scored_result = chain.invoke({"question": question, "context": docs})

    score = scored_result.binary_score

    if score == "yes":
        print("---DECISION: DOCS RELEVANT---")
        return "generate"

    else:
        print("---DECISION: DOCS NOT RELEVANT---")
        print(score)
        return "rewrite"
    

# ------------------ Agent node ----------------------------

def agent(state):
    """
    Invokes the agent model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply end.
    Args:
        state (messages): The current state
    Returns:
        dict: The updated state with the agent response appended to messages
    """
    print("---CALL AGENT---")
    messages = state["messages"]

    llm_with_tools = llm.bind_tools(tools, tool_choice="required")
    response = llm_with_tools.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

#---------------------- rewrite node -------------

def rewrite(state):
    """
    Transform the query to produce a better question.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with re-phrased question
    """

    print("---TRANSFORM QUERY---")
    messages = state["messages"]
    question = messages[0].content

    msg = [
        HumanMessage(
            content=f""" \n 
    Look at the input and try to reason about the underlying semantic intent / meaning. \n 
    Here is the initial question:
    \n ------- \n
    {question} 
    \n ------- \n
    Formulate an improved question: """,
        )
    ]

    # Grader
    response = llm.invoke(msg)
    return {"messages": [response]}

#----------------------------- generate node ------------------------------

def generate(state):
    """
    Generate answer

    Args:
        state (messages): The current state

    Returns:
         dict: The updated state with re-phrased question
    """
    print("---GENERATE---")
    messages = state["messages"]
    question = messages[0].content
    last_message = messages[-1]

    docs = last_message.content

    # Prompt
    prompt = hub.pull("rlm/rag-prompt")

    # Post-processing
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Chain
    rag_chain = prompt | llm | StrOutputParser()

    # Run
    response = rag_chain.invoke({"context": docs, "question": question})
    return {"messages": [response]}

#-------------------- GRAPH -------------------

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