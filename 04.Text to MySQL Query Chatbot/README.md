
# 1️⃣ Text to MySQL query

## Description
This project is an AI-powered MySQL query agent that allows users to interact with a database using natural language queries. It leverages LangChain, Ollama, and LangGraph to generate, execute, and interpret SQL queries from user input. The project utilizes the Chinook database, a sample SQLite database for practicing SQL operations.

- This simple agent responds to a text message with a MySQL query execution result.
- he agent is built using LangGraph
- We will start with simple linear flow and then add more complex flows
- For this example, We will use Chinook database which is sample database available for sqlite
- You can tryout this for any database sqlite or mysql or postgresql by changing the connection string
 **1. Chinook database**

 [Chinook Sample Data - Yugabyte Docs](https://docs.yugabyte.com/preview/sample-data/chinook/)

- Representation

 ![Alt text](chinook-er-diagram.png)

 **2. Ollama model** 
- Information
 [Qwen2.5 Model - Ollama Library](https://ollama.com/library/qwen2.5)

```sh
ollama pull qwen2.5 
```

**3. Smith Langchain**

- [LangChain Hub - Smith](https://smith.langchain.com/hub?organizationId=5efcb3f2-4211-5c65-9df5-a364130)

- [Smith LangChain](https://smith.langchain.com/hub/langchain-ai/sql-query-system-prompt?organizationId=5efcb3f2-4211-5c65-9df5-a3641303ab89)



**4. Chat prompt template**
- [SQL Query System Prompt - LangChain Hub](https://smith.langchain.com/hub/langchain-ai/sql-query-system-prompt?organizationId=5efcb3f2-4211-5c65-9df5-a3641303ab89)

```python
query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
#print("query prompt template-> ",query_prompt_template)
query_prompt_template.messages[0].pretty_print()
```
**Output:**

```sh
================================ System Message ================================

Given an input question, create a syntactically correct {dialect} query to run to help find the answer. Unless the user specifies in his question a specific number of examples they wish to obtain, always limit your query to at most {top_k} results. You can order the results by a relevant column to return the most interesting examples 
in the database.

Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.

Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Only use the following tables:
{table_info}

Question: {input}
```
- [smith.langchain.com](https://smith.langchain.com/hub/langchain-ai/sql-agent-system-prompt?organizationId=5efcb3f2-4211-5c65-9d5f-a3641303ab89)

```python
prompt = hub.pull("langchain-ai/sql-agent-system-prompt")
#print("query prompt template-> ",prompt)
prompt.messages[0].pretty_print()
```
**Output:**

```sh
================================ System Message ================================

You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

To start you should ALWAYS look at the tables in the database to see what you can query.
Do NOT skip this step.
Then you should query the schema of the most relevant tables.
```

**5. Aplication State or Graph State**

```python
query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
print("query prompt template-> ",query_prompt_template)
query_prompt_template.messages[0].pretty_print()
```

## Features
- **Natural Language to SQL:** Converts user questions into SQL queries using an LLM.
- **Database Interaction:** Executes SQL queries on the Chinook database.
- **Intelligent Response Generation:** Uses AI to interpret and provide human-readable answers.
- **Graph-Based Execution Flow:** Uses LangGraph to structure the process.
- **Error Recovery:** Handles query failures and regenerates them.


### Write, Execute and Generate MySQL Response
1. Write node for MySQL Query

## Requirements
```sh
Python 3.8+
pip install -r requirements.txt
Ollama LLM server running locally (http://localhost:11434)
Internet access to download the Chinook database
```

## Installation
```sh
git clone https://github.com/your-repo/text-to-mysql-agent.git
cd text-to-mysql-agent
pip install -r requirements.txt
cp .env.example .env
# Update .env with necessary credentials
python Text_to_MySQL_Agent.py
```

## Architecture
1. **Query Generation:** The LLM generates a valid SQL query.
2. **Execution:** The SQL query runs on the database.
3. **Answer Generation:** The AI interprets the results and responds in natural language.

## Dependencies
```sh
LangChain
Ollama
LangGraph
SQLAlchemy
Requests
```

## MySQL query bot

**1. Write the query**
```python
question = "How many employees are there?"
query = write_query({"question": question})
print(query)
```
Ouput:

```sh
{'query': 'SELECT COUNT(*) AS NumberOfEmployees FROM Employee;'}
```
**2. Execute the query**
``` python
result = execute_query(query)
print(result)
```
Ouput:
```sh
{'result': '[(8,)]'}
```

**3. Combine all information into a state dictionary**
``` python
state_dict= {"question": question, **query, **result}
print("state ->",state_dict)
```
Ouput:
```sh
{'question': 'how many employees are there?', 'query': 'SELECT COUNT(*) FROM Employee', 'result': '[(8,)]'}
```

**4. Generate the query**
``` python
state = {"question": question, **query, **result}
answer = generate_answer(state)
print(answer)
```
**Ouput:**
```sh
{'answer': 'Based on the provided SQL query and result, there are 8 employees in total.'}
```

## Building the graph

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

![Alt text](assets/esquema2.JPG)

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

## LangGraph AGENTS: Automating query execution with AI

- **Agents can:**
  - Query the database multiple times to refine their answer.
  - Recover from errors by detecting failed queries and regenerating them.
  - Answer questions based on both schema structure and database content.
  - They can query the database as many times as needed to answer the user question.
  - They can recover from errors by running a generated query, catching the traceback and regenerating it correctly.
  - They can answer questions based on the databases' schema as well as on the databases' content (like describing a specific table).

- **Flow representation**

![Alt text](assets/esquema1.JPG)

### **Steps**

**1. BLAH BLAH**
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
**2. BLAH BLAH**
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

- Key Descriptions:
  - table_info: Contains a large text block with SQL statements to create the database tables, including relationships (PRIMARY KEY, FOREIGN KEY) and sample data (3 rows per table).
  - table_names: A string listing all table names in the database, separated by commas.

- Content of table_info
  - Includes the structure of several tables such as Album, Artist, Customer, Employee, Genre, Invoice, InvoiceLine, MediaType, Playlist, PlaylistTrack, and Track.
  - Contains CREATE TABLE statements detailing columns, data types, and primary/foreign keys.
At the end of each table definition, there is a comment (/* ... */) with three sample rows.

**3. BLAH BLAH**
``` python
tools = toolkit.get_tools()
print("tools-> ",tools)
```

**Ouput:**
```sh
blah blha
```

**4. BLAH BLAH**
``` python
##
```
**Ouput:**
```sh
blah blha
```