
# General: Text to MySQL query chatbot

## Description

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

This project is a MySQL Query Bot that automatically generates, executes, and processes database queries based on user input. It uses utility functions to generate SQL queries, execute them on a database, and format responses into readable answers.

## Usage
1. Modify the `user_question` variable in `mysql_query_bot.py` to reflect your query.
2. Run the script with the following command:

```sh
   python mysql_query_bot.py
```


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

### Document Chunking

**1. Text splitter structure**
```sh
[
    "TokenTextSplitter",
    "TextSplitter",
    "Tokenizer",
    "Language",
    "RecursiveCharacterTextSplitter",
    "RecursiveJsonSplitter",
    "LatexTextSplitter",
    "PythonCodeTextSplitter",
    "KonlpyTextSplitter",
    "SpacyTextSplitter",
    "NLTKTextSplitter",
    "split_text_on_tokens",
    "SentenceTransformersTokenTextSplitter",
    "ElementType",
    "HeaderType",
    "Line
```
**1. blah blah**
``` python
```
**Ouput:**
```sh
```

**1. blah blah**
``` python
```
**Ouput:**
```sh
```

**1. blah blah**
``` python
```
**Ouput:**
```sh
```
### Document Vector Embedding

**1. blah blah**
``` python
```
**Ouput:**
```sh
```

**1. blah blah**
``` python
```
**Ouput:**
```sh
```

**1. blah blah**
``` python
```
**Ouput:**
```sh
```

# 2️⃣ Building the graph

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
   python building_graph.py
```


## Implementation
**1. Build the processing graph**
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

### **1. System promp**
``` python
system_prompt = prompt.invoke({'dialect': db.dialect, 'top_k': 5})
print("system_prompt-> ",system_prompt)
```

```json
{
  "messages": [
    {
      "type": "SystemMessage",
      "content": "You are an agent designed to interact with a SQL database.\nGiven an input question, create a syntactically correct fies a specific number of  ......  database.\n\nTo start you should ALWAYS look at the tables in the database to see what you can query.\nDo NOT skip this step.\nThen you should query the schema of the most relevant tables.",
      "additional_kwargs": {},
      "response_metadata": {}
    }
  ]
}
```
### **2. Retrieve Available Tools**
``` python
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
print("toolkit context-> ",toolkit.get_context())
```

**Ouput:**
```sh
{
    "table_info": "..."
    "table_names": "..."
}
```

- **Key Descriptions:**
  - table_info: Contains a large text block with SQL statements to create the database tables, including relationships 
  - table_names: A string listing all table names in the database, separated by commas.


``` python
tools = toolkit.get_tools()
print("tools-> ",tools)
```

**Ouput:**
```sh
tools_dict = [
    { "name": "QuerySQLDatabaseTool",},
    { "name": "InfoSQLDatabaseTool", },
    { "name": "ListSQLDatabaseTool", },
    { "name": "QuerySQLCheckerTool",
        "description":
        "db": "<SQLDatabase object at 0x000001FAFFEACEF0>",
        "llm": {
            "model": "qwen2.5",
            "base_url": "http://localhost:11434"
        },
        "llm_chain": {
            "verbose": False,
            "prompt": {
                "input_variables": ["dialect", "query"],
                "template": (
                    "\n{query}\nDouble check the {dialect} query above for common mistakes, including:\n"
                    ....
                    "Output the final SQL query only.\n\nSQL Query: "
                )
            },
        }
    }
]

```
- **QuerySQLDatabaseTool** – Executes SQL queries and handles errors. If a query fails, it suggests corrections.
- **InfoSQLDatabaseTool** – Retrieves table schemas and sample data. Ensures tables exist before querying.
- **ListSQLDatabaseTool** – Lists all available tables in the database.
- **QuerySQLCheckerTool** – Validates SQL queries using an LLM (qwen2.5). Detects and fixes common mistakes before execution.

### **3. Execute an SQL Query**
``` python
# Invoke the first tool to execute an SQL query selecting two rows from the "Album" table
tools[0].invoke("select * from Album LIMIT 2")
# The following line is commented out; it seems to be invoking another tool with table names
# print(tools[1].invoke("Album,Customer"))
```
**Ouput:**
```sh
[(1, 'For Those About To Rock We Salute You', 1), (2, 'Balls to the Wall', 2)]
```

### **4. Create the ReAct Agent**
- The ReAct agent (Reasoning + Acting agent) is created using:
  - llm: A large language model (e.g., GPT).
  - tools: The available tools (including the SQL executor).
  - system_prompt: A predefined prompt that guides the agent’s behavior.
- This agent is designed to reason about a query and take the appropriate action.

``` python
agent_executor = create_react_agent(llm, tools, state_modifier=system_prompt)
save_and_open_graph(agent_executor, filename="assets/agent_graph.png") # Save and open the graph image
```

![Alt text](assets/agent_graph.png)

### **5. Define and Process a User Query**
``` python
# Stream the agent's responses step by step while processing the query
for step in agent_executor.stream(query, stream_mode="updates"):
    print(step)  # Print each step of the execution
    #prints the last message in the response
    step['messages'][-1].pretty_print()
```
**Ouput:**

**1. Agent ('agent') – The LLM (AI model) generates or processes a query.**
```sh
step->  {'agent': {'messages': [AIMessage(content='', response_metadata={'model': 'qwen2.5', ...})]}}
```

- El agente comienza con un mensaje vacío.
- Está usando el modelo qwen2.5.
- Ejecuta una llamada a la herramienta `sql_db_list_tables` para obtener la lista de tablas disponibles.

**2. Tool ('tools') – The tool responds with results.**

```sh
"messages": [
    ToolMessage(
        content="Album, Artist, Customer, Invoice...",  # Tool output
        name="sql_db_list_tables",  # Tool used
    )
]
```
- Se obtiene la lista de tablas
- Mensaje de herramienta: Album, Artist, Customer, Employee, Genre, Invoice, InvoiceLine, MediaType, Playlist, PlaylistTrack, Track

**3.  Agent ('agent') – Agent Requests More Details – Queries schema of specific tables.**
- Mensaje del agente: 
    - AIMessage: Representa un mensaje del asistente AI.
        - tool_calls: Indica si el agente ha llamado a una herramienta para realizar una acción.
- Ahora, el agente quiere más detalles sobre las tablas Invoice y Customer, porque parecen relevantes para la consulta de compras por país.


**4. Tool ('tools') –  Tool Responds with Schema Details.**
```sh
step->  {'tools': {'messages': [ToolMessage(content='CREATE TABLE "Customer" (...), CREATE TABLE "Invoice" (...')]}}
```
- El sistema responde con la estructura de las tablas `Customer` e `Invoice`.
- También muestra tres registros de ejemplo de cada tabla, lo que ayuda al agente a entender la información.

**5. Agent ('agent') –  Agent Checks Query Validity.**
- Mensaje del agente: 
```sh
{
    "agent": {
        "messages": [
            AIMessage(
                tool_calls=[
                    {
                        "name": "sql_db_query_checker",
                        "args": {
                            "query": "SELECT C.Country, COUNT(I.InvoiceId) AS PurchaseCount FROM Customer C INNER JOIN Invoice I ON C.CustomerId = I.CustomerId GROUP BY C.Country ORDER BY PurchaseCount DESC LIMIT 5"
                        },
                        "id": "478e4a57-016d-4b2f-b5bc-d861398e0f85",
                        "type": "tool_call"
                    }
                ]
            )
        ]
    }
}
```
- Basándose en la estructura de las tablas, el agente genera la siguiente consulta SQL:
``` sql
SELECT Customer.Country, COUNT(*) AS purchase_count 
FROM Invoice 
JOIN Customer ON Invoice.CustomerId = Customer.CustomerId 
GROUP BY Customer.Country 
ORDER BY purchase_count DESC 
LIMIT 5;
```
- Luego, pasa esta consulta al comprobador de consultas SQL para verificar si está bien escrita.

**6. Tool ('tools') – Tool Confirms Query is Correct.**

- La herramienta confirma que la consulta es válida y no tiene errores.
- Mensaje de herramienta: The provided SQL query does not contain any common mistakes based on the conditions you've listed. Here is the original query:


```sh
step->  {'tools': {'messages': [ToolMessage(content='The provided SQL query appears to be correctly written ...')]}}
```
- La herramienta confirma que la consulta es válida y no tiene errores.

**7.  Agent ('agent') – .**

```sh
step->  {'agent': {'messages': [..., 'tool_calls': [{'name': 'sql_db_query', 'args': {'query': 'SELECT Customer.Country, COUNT(*) ...'}]}}

```
- Como la consulta SQL es válida, el agente procede a ejecutarla.

**8. Tool ('tools') – .**

```sh
step->  {'tools': {'messages': [ToolMessage(content="[('USA', 91), ('Canada', 56), ('France', 35), ('Brazil', 35), ('Germany', 28)]"]}}
```
- Mensaje de herramienta: [('USA', 91), ('Canada', 56), ('France', 35), ('Brazil', 35), ('Germany', 28)]

**9.  Agent ('agent') –  Agent Generates Final Answer.**
- Finalmente, el agente genera su respuesta:
- Mensaje del agente: The country with the most purchases is USA, followed by Canada, France, Brazil, and Germany. Here are the top 5 countries based on the number of purchases:
```sh
{
    "agent": {
        "messages": [
            AIMessage(
                content="The country with the most purchases is USA, followed by Canada, France, Brazil, and Germany. Here are the top 5 countries based on purchase count:\n\n1. USA - 91 purchases\n2. Canada - 56 purchases\n3. France - 35 purchases\n4. Brazil - 35 purchases\n5. Germany - 28 purchases"
            )
        ]
    }
}

```

## 🔍 Resumen de la ejecución
- 📌 El agente descubre la base de datos (lista de tablas).
- 🔎 Obtiene los esquemas de las tablas relevantes (Invoice y Customer).
- 🧠 Genera una consulta SQL para contar compras por país.
- ✅ Verifica la consulta para asegurarse de que está bien escrita.
- ⚡ Ejecuta la consulta y obtiene los resultados.
- 🏆 Devuelve la respuesta final: EE.UU. es el país con más compras.