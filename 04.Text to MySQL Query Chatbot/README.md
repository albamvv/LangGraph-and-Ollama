
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

**4. Chat prompt template**
[SQL Query System Prompt - LangChain Hub](https://smith.langchain.com/hub/langchain-ai/sql-query-system-prompt?organizationId=5efcb3f2-4211-5c65-9df5-a3641303ab89)

**5. Flow**
![Alt text](assets/esquema1.JPG)

**6. Aplication State or Graph State**

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


## Usage
### **Create a Python script or interactive session and run:**

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
Ouput:
```sh
{'answer': 'Based on the provided SQL query and result, there are 8 employees in total.'}
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


## Building the graph
```python
# Build the processing graph
graph_builder = StateGraph(State)
graph_builder.add_node("write_query", write_query)
graph_builder.add_node("execute_query", execute_query)
graph_builder.add_node("generate_answer", generate_answer)

# Define the execution flow of the graph
graph_builder.add_edge(START, "write_query")
graph_builder.add_edge("write_query", "execute_query")
graph_builder.add_edge("execute_query", "generate_answer")

# Compile and visualize the graph
graph = graph_builder.compile()
```

![Alt text](assets/esquema2.JPG)

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
