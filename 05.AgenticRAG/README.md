
# General: Argentic RAG

## Description

ollama pull nomic-embed-text
## Features

## Requirements

## Installation

## Architecture

## Dependencies
```sh
LangChain
Ollama
LangGraph
SQLAlchemy
Requests
```

# 1️⃣Vector Stores an Retrieve

## Overview


## Usage
¡

```sh
python 1.Vector_Stores_and_Retrievals.py
```
## Resume

- Carga y extrae texto de PDFs en rag-dataset.
- Divide el texto en fragmentos (chunks) de 1000 caracteres con solapamiento.
- Convierte los fragmentos en vectores mediante embeddings.
- Crea un índice FAISS para almacenar los vectores.
- Agrega los vectores de los fragmentos al índice.
- Realiza una búsqueda semántica basada en una consulta.
- Guarda el índice FAISS localmente.

## Implementation

### Document Loader
**1. Vector Stores and Retrievals**

- ![Alt text](assets/tool_document_ingestion.png)

``` python
loader = PyMuPDFLoader(r"rag-dataset\gym supplements\1. Analysis of Actual Fitness Supplement.pdf")
loader.load()
```

- This dictionary represents a list of `Document` objects, where each object contains two main elements:

- `metadata` (dictionary): Contains information about the document, such as:
    - `producer`: The software used to generate the document (e.g., iLovePDF).
    - `creator`: The creator of the document (empty in this case).
    - `creationdate`, `moddate`, `modDate`: Creation and modification dates.
    - `source`, `file_path`: File path in the system.
    - `total_pages`: Total number of pages in the document.
    - `format`: PDF format.
    - `title`, `author`, `subject`, `keywords`: Bibliographic information.
    - `page`: The specific page number this `Document` represents.

**2. PDFs**
- Buscar PDFs en el directorio "rag-dataset"

``` python
pdfs = []  # Initialize an empty list to store PDF file paths

for root, dirs, files in os.walk("rag-dataset"):  
    # os.walk() iterates through all directories and files inside "rag-dataset"
    # root -> The current folder being scanned  
    # dirs -> List of subdirectories in the current folder  
    # files -> List of files in the current folder  

    # Loop through all files in the current directory  
    for file in files:  
        if file.endswith(".pdf"):  # Check if the file has a ".pdf" extension  
            pdfs.append(os.path.join(root, file))  # Store the full file path  

print("pdf: ", pdfs)  # Print the list of PDF file paths  
```
Ouput:
```sh
pdf:  ['rag-dataset\\finance\\amazon\\amazon-10-q-q3-2024.pdf', 'rag-dataset\\finance\\facebook\\Earnings-Presentation-Q3-2024.pdf', 'rag-dataset\\finance\\facebook\\Meta-09-30-2024-Exhibit-99-1_FINAL.pdf', 'rag-dataset\\finance\\facebook\\META-Q3-2024-Earnings-Call-Transcript.pdf', 'rag-dataset\\finance\\facebook\\META-Q3-2024-Follow-Up-Call-Transcript.pdf', 'rag-dataset\\finance\\google\\goog-10-q-q3-2024.pdf', 'rag-dataset\\gym supplements\\1. Analysis of Actual Fitness Supplement.pdf', 'rag-dataset\\gym supplements\\2. High Prevalence of Supplement Intake.pdf', 'rag-dataset\\health supplements\\1. dietary supplements - for whom.pdf', 'rag-dataset\\health supplements\\2. Nutraceuticals research.pdf', 'rag-dataset\\health supplements\\3.health_supplements_side_effects.pdf']
```
- Cargar cada PDF con PyMuPDFLoader 

``` python
docs = []
for pdf in pdfs:  # Loop through each PDF file path stored in the pdfs list
    loader = PyMuPDFLoader(pdf)  # Create a PDF loader using PyMuPDFLoader
    temp = loader.load()  # Load the content of the PDF (extract text and metadata)
    docs.extend(temp)  # Add the extracted content to the docs list
```   
- `docs` contendrá todos los textos extraídos de los PDFs.

### Document Chunking and embedding

**1. Text splitter structure**
```sh
    "TokenTextSplitter", "TextSplitter", "Tokenizer", "Language", "RecursiveCharacterTextSplitter", "RecursiveJsonSplitter",
    "LatexTextSplitter", "PythonCodeTextSplitter", "KonlpyTextSplitter", "SpacyTextSplitter", "NLTKTextSplitter", 
    "split_text_on_tokens", "SentenceTransformersTokenTextSplitter", "ElementType", "HeaderType", "Line
```
**2. Chunking**

-   RecursiveCharacterTextSplitter:
    - Divide los documentos en fragmentos de 1000 caracteres.
    - Se superponen 100 caracteres entre fragmentos para contexto.
- `chunks` contendrá los fragmentos generados

``` python
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(docs)
```

- **Ejemplo conceptual**
``` python
chunks[0].page_content = "Protein is essential for muscle growth. A diet rich in lean meats, eggs, and legumes helps build muscle mass."
chunks[1].page_content = "A diet rich in lean meats, eggs, and legumes helps build muscle mass. Strength training also plays a key role."
```

**3. Vectorización de documentos**
- Convierte el texto del primer fragmento (`chunks[0].page_content`) en un vector numérico.
- `vector` representa el contenido semántico del texto en una matriz de números, es la representación matemática de un `chunk` en un espacio de alta dimensión.
    - `vector = [0.234, -0.875, 0.562, 1.134, -0.782, ...] `
``` python
vector = embeddings.embed_query(chunks[0].page_content)
```

**4. Creación de un índice FAISS**
- `faiss.IndexFlatIP(d)`:
    - Crea un índice FAISS basado en el Producto Interno (`IP` = Inner Product).
    - `len(vector)`: Dimensión del vector de embeddings.
- FAISS necesita un espacio vectorial uniforme: Todos los vectores en el índice deben tener la misma cantidad de dimensiones.
- Si las dimensiones no coinciden, FAISS generará un error.

``` python
index = faiss.IndexFlatIP(len(vector))
```

**5. Creación de FAISS Vector Store**
- Se crea un almacén de vectores `FAISS` con:
    - `embedding_function=embeddings`: Función de embeddings para convertir textos en vectores.
    - `index=index`: Índice FAISS donde se almacenarán los vectores.
    - `docstore=InMemoryDocstore()`: Almacén de documentos en memoria.
    - `index_to_docstore_id={}`: Diccionario vacío para mapear IDs de FAISS a documentos.

``` python
vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)
```
- Agregar documentos al indice FAISS
    - Agrega los fragmentos (`chunks`) al índice FAISS.
    - Genera un ID único para cada fragmento agregado.
    - Devuelve una lista de IDs (`ids`) asignados a cada documento agregado.

``` python
ids = vector_store.add_documents(documents=chunks)
```

**Output**
``` python
ids-> ['doc_1', 'doc_2', 'doc_3', ..., 'doc_N']
```

**6. Busqueda de documentos relevantes**

- Busca los 5 documentos más similares a la pregunta `"how to gain muscle mass?"`.
- `search_type='similarity'`: Usa similitud de coseno o producto interno para recuperar los documentos más cercanos semánticamente.
- FAISS devuelve los IDs de los 5 fragmentos más relevantes.
- Con esos IDs, podemos recuperar el contenido original de los fragmentos.

``` python
question = "how to gain muscle mass?"
result = vector_store.search(query=question, k=5, search_type='similarity')
```

**7. Guarda el indice FAISS**
- Guarda el índice FAISS en una base de datos para uso futuro.

``` python
vector_store.save_local(db_name)
```

# 2️⃣ Argentic RAG

## Overview

This project constructs a processing graph to handle query execution using `langgraph`. It defines a sequence of steps to:
1. Write a query.
2. Execute the query.
3. Generate an answer from the results.

![Alt text](assets/building_graph.JPG)

## Files

- `building_graph.py`: Main script to build and execute the graph.
- `query_utils.py`: Contains helper functions for query handling.
- `config.py`: Defines the State used in the graph.

## Usage

```sh
   python 2.ArgenticRAG.py
```


## Implementation
**1. Argentic RAG**
```python
graph_builder = StateGraph(State)
graph_builder.add_node("write_query", write_query)
graph_builder.add_node("execute_query", execute_query)
graph_builder.add_node("generate_answer", generate_answer)
```

**2. Define the execution flow of the graph**
```python
graph_builder.add_edge(START, "write_query")
graph_builder.add_edge("write_query", "execute_query")
graph_builder.add_edge("execute_query", "generate_answer")
```
**3. Compile and visualize the graph**
```python
graph = graph_builder.compile()
```
**4. Graph schema**

START → Write SQL Query → Execute SQL Query → Generate Answer → END

**5. Example: Query to list all albums**
``` python
query = {'question': 'List all the albums'}
for step in graph.stream(query, stream_mode="updates"):
    print(step)
```
**Output**

```json
{
    "write_query": {
        "query": "SELECT * FROM Album"
    },
    "execute_query": {
        "result": [
            [1, "For Those About To Rock We Salute You", 1],
            [2, "Balls to the Wall", 2],
            [3, "Restless and Wild", 2],
            [4, "Let There Be Rock", 1],
            [5, "Big Ones", 3],
            [6, "Jagged Little Pill", 4],
            [7, "Facelift", 5],
            [8, "Warner 25 Anos", 6],
            [9, "Plays Metallica By Four Cellos", 7],
            [10, "Audioslave", 8]
        ]
    },
    "generate_answer": {
        "answer": "It seems like you've provided a list of tracks or songs with their respective numbers and details. Would you like me to do something specific with this information, such as organize it in a certain way, find patterns, or answer a particular question about it?"
    }
}
```

# 3️⃣ LangGraph AGENTS: Automating query execution with AI

## Overview

This project uses LangGraph and LangChain to build an AI-powered agent capable of querying an SQL database intelligently. The agent can:
- Perform iterative database queries to refine results.
- Detect and recover from query errors.
- Answer questions based on the database structure and content.

- **Agents can:**
  - Query the database multiple times to refine their answer.
  - Recover from errors by detecting failed queries and regenerating them.
  - Answer questions based on both schema structure and database content.
  - They can query the database as many times as needed to answer the user question.
  - They can recover from errors by running a generated query, catching the traceback and regenerating it correctly.
  - They can answer questions based on the databases' schema as well as on the databases' content (like describing a specific table).

- **Flow representation**

![Alt text](assets/esquema1.JPG)

## Files

- `langraph_agent.py`: The main script that sets up and executes the AI agent.
- `config.py`: Defines database and prompt configurations.
- `query_utils.py`: Contains helper functions for query handling.

## Usage

```sh
   python langraph_agent.py
```

## Implementation


### Retrieve**

- **Load vector**
    - `FAISS.load_local(db_name, embeddings)`:
        - Carga un índice FAISS previamente guardado en la base de datos db_name.
        - Usa `embeddings` para convertir nuevas consultas en vectores y compararlos con los almacenados.
    - allow_dangerous_deserialization=True:
        - Permite cargar FAISS desde un archivo local sin restricciones de seguridad.
```python
    vector_store = FAISS.load_local(db_name, embeddings, allow_dangerous_deserialization=True)
```
- **Retriever**
    - `as_retriever(search_type="similarity")`:
        - Convierte `vector_store` en un sistema de recuperación basado en FAISS.
        - `search_type="similarity"`: Utiliza similitud de coseno o producto interno para encontrar fragmentos relevantes.
    - `search_kwargs = {'k': 5}`:
        - Recupera los 5 fragmentos más similares a la consulta.
```python
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs = {'k': 5})
```
- **Load question and invoke**
```python
    question = "how to gain muscle mass?"
    retriever.invoke(question)
```
- **Retrieval as a tool**

```python
    retriever_tool = create_retriever_tool(
    retriever,
    "health_supplements",
    "Search and retrun information about the Health Supplements for workout and gym",
    )
    tools = [retriever_tool]
```
### Agent**
- **Flow** : we can lay out an agentic RAG graph like this
    - The state is a set of messages
    - Each node will update (append to) state
    - Conditional edges decide which node to visit next

![Alt text](assets/agent_flow.png)


**1. Document grader**
**2. Agent Node**
**3. Rewrite Node**
**1. Generate Node**


### **Graph**
**1. Introduction**
- Start with an agent, call_model
- Agent make a decision to call a function
- If so, then action to call tool (retriever)
-Then call agent with the tool output added to messages (state) 

- ![Alt text](assets/agent_tool_graph.png)


