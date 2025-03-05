
# 1️⃣ Tool calling

## Overview

This script demonstrates how to integrate an LLM (Large Language Model) with various tools to process and respond to queries. The model is configured using ChatOllama and can dynamically invoke functions such as arithmetic operations and web searches.
- https://python.langchain.com/docs/integrations/tools/

- LLM Automatically calls the function based on the query
- Function parameters are automatically passed to the function
- It is one of the essential requirements of the Agent
- Not all LLM supports tool calling.

![Alt text](assets/tool_calling.JPG)

## Key Features
1. **Tool Creation and Invocation**
- Functions (add, multiply, etc.) are defined and bound to the LLM, allowing it to automatically call them when needed.
- The model can interpret user queries and decide whether a tool should be used for calculations or searches.
- https://python.langchain.com/docs/integrations/tools/ 


2. **Built-in Search Integration**
- Includes search tools like Wikipedia, PubMed, and Tavily for retrieving information.
- PubMed® comprises more than 35 million citations for biomedical literature from MEDLINE, life science journals, and online books.
- DuckDuckDuck

```bash
search = DuckDuckGoSearchRun()
```
- DuckDuckGoSearchRun, una herramienta de búsqueda en línea basada en el motor de DuckDuckGo
- Crea una instancia de DuckDuckGoSearchRun, que es una clase utilizada en LangChain para ejecutar búsquedas en DuckDuckGo.
- Esta clase permite realizar búsquedas en la web sin rastreo, a diferencia de Google.

```bash
search.invoke("What is today's stock market news?")
```
- Ejecuta la búsqueda con la consulta "What is today's stock market news?".
- Retorna los resultados de la búsqueda en tiempo real.

3. **Handling Tool Calls**
- Queries are processed by checking if a tool needs to be invoked.
- The script extracts the required tool's name, executes it, and appends the results to the conversation.
- The LLM is reinvoked with the updated context to generate a final response.

## Workflow
1. Define and register tools.
```bash
tools = [wikipedia_search, pubmed_search, tavily_search, multiply2]
list_of_tools = {tool.name: tool for tool in tools}
```
2. Bind tools to the LLM.
- bind_tools(tools) links the model (llm) with the available tools (e.g., Wikipedia search, PubMed search, Tavily search, or a multiplication function).
- Now, the LLM can automatically decide whether a tool should be used to answer a query.
```bash
llm_with_tools = llm.bind_tools(tools)
```
3. Process user queries:
- Determine if a tool is required.
- Invoke the appropriate tool.
```bash
response = llm_with_tools.invoke(query5)
```
- Append the tool's response.
```bash
messages.append(tool_calls_response) 
```
- Reinvoke the LLM with the enriched conversation.
```bash
response = llm_with_tools.invoke(messages)
```

4. Display the final response.




### Generate Final Result with Tool Calling

```bash 
query = "What is medicine for lung cancer?"
messages = [HumanMessage(query)]
```
![Alt text](assets/messages1.JPG)

```bash 
ai_msg = llm_with_tools.invoke(messages)
messages.append(ai_msg) # Append AI's response to the messages
```
![Alt text](assets/messages2.JPG)

```bash 
for tool_call in ai_msg.tool_calls:
    name = tool_call['name'].lower()  # Get the tool name
    selected_tool = list_of_tools[name]  # Find the tool from the dictionary
    tool_msg = selected_tool.invoke(tool_call)  # Execute the tool
    messages.append(tool_msg)  # Append the tool response
```

![Alt text](assets/messages3.JPG)

```bash 
# Se vuelve a invocar al LLM con la nueva información
response = llm_with_tools.invoke(messages)
print("Response->" ,response.content)
```
![Alt text](assets/response.JPG)

