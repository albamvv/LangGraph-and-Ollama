
# 1️⃣ Text to MySQL query

## Description
This project is an AI-powered MySQL query agent that allows users to interact with a database using natural language queries. It leverages LangChain, Ollama, and LangGraph to generate, execute, and interpret SQL queries from user input. The project utilizes the Chinook database, a sample SQLite database for practicing SQL operations.

- This simple agent responds to a text message with a MySQL query execution result.
- he agent is built using LangGraph
- We will start with simple linear flow and then add more complex flows
- For this example, We will use Chinook database which is sample database available for sqlite
- You can tryout this for any database sqlite or mysql or postgresql by changing the connection string
- Chinook database -> docs.yugabyte.com/preview/sample-data/chinook/

 ![Alt text](chinook-er-diagram.png)
- Ollama model -> https://ollama.com/library/qwen2.5 
- ollama pull qwen2.5 

 ![Alt text](assets/esquema1.JPG)
  ![Alt text](assets/esquema2.JPG)
- smith.langchain.com/hub?organizationId=5efcb3f2-4211-5c65-9df5-a3641303ab89
-chat promp template -> https://smith.langchain.com/hub/langchain-ai/sql-query-system-prompt?organizationId=5efcb3f2-4211-5c65-9df5-a3641303ab89 
 
## Features
- **Natural Language to SQL:** Converts user questions into SQL queries using an LLM.
- **Database Interaction:** Executes SQL queries on the Chinook database.
- **Intelligent Response Generation:** Uses AI to interpret and provide human-readable answers.
- **Graph-Based Execution Flow:** Uses LangGraph to structure the process.
- **Error Recovery:** Handles query failures and regenerates them.
## Others

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
Create a Python script or interactive session and run:
```python
from Text_to_MySQL_Agent import write_query, execute_query, generate_answer

question = "How many employees are there?"
query = write_query({"question": question})
print(query)

result = execute_query(query)
print(result)

state = {"question": question, **query, **result}
answer = generate_answer(state)
print(answer)
```

## Example Output
```sh
{'query': 'SELECT COUNT(*) AS NumberOfEmployees FROM Employee;'}
{'result': '[(8,)]'}
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


