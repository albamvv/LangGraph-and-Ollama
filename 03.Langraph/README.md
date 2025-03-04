# LangGraph-and-Ollama
This Python script sets up a chatbot using LangChain and the Ollama model. 
It loads environment variables, initializes a language model (llama3.2:3b), and defines a chatbot function that processes user messages. 
A state graph is built using StateGraph to manage conversation flow. The chatbot receives input, generates responses, 
and maintains conversation history. The graph structure is visualized using IPython. 
The script includes a loop for continuous user interaction, allowing users to chat with the bot until they exit by typing 'q', 'quit', or 'exit'.
- https://langchain-ai.github.io/langgraph/reference/graphs/
- https://python.langchain.com/docs/tutorials/llm_chain/ 

## 1️⃣ Tool calling

- LLM Automatically calls the function based on the query
- Function parameters are automatically passed to the function
- It is one of the essential requirements of the Agent
- Not all LLM supports tool calling.

![Alt text](assets/tool_calling.JPG)

### Custom Tools
### Calling In-Built 
#### DuckDuckGo Search
- https://python.langchain.com/docs/integrations/tools/ 
- DuckDuckGoSearchRun, una herramienta de búsqueda en línea basada en el motor de DuckDuckGo
- search = DuckDuckGoSearchRun()
Crea una instancia de DuckDuckGoSearchRun, que es una clase utilizada en LangChain para ejecutar búsquedas en DuckDuckGo.
Esta clase permite realizar búsquedas en la web sin rastreo, a diferencia de Google.

- search.invoke("What is today's stock market news?")
Ejecuta la búsqueda con la consulta "What is today's stock market news?".
Retorna los resultados de la búsqueda en tiempo real.

#### Tavily Search
#### Wikipedia
#### PubMed
PubMed® comprises more than 35 million citations for biomedical literature from MEDLINE, life science journals, and online books. Citations may include links to full text content from PubMed Central and publisher web sites.
#### Tool Calling with LLM

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

## 2️⃣ LanGraph 🦜🕸️ Chatbot with LangChain and LangGraph



This repository contains a Python script that implements a chatbot using **LangChain**, **LangGraph**, and the **Ollama (llama3.2:3b)** model.  
The chatbot manages conversations using a state graph and allows continuous interaction with the user.

### 📌 Requirements

Before running the script, make sure you have the following dependencies installed:

```bash
pip install langchain langgraph python-dotenv
```

Also, the **Ollama** server must be running at `http://localhost:11434`.

### 🚀 Execution

1. **Configure environment variables**: The script loads variables from a `.env` file. Set the following variables if needed:
   ```env
   LANGCHAIN_API_KEY=your_api_key
   LANGCHAIN_ENDPOINT=your_endpoint
   LANGSMITH_TRACING=false
   ```

2. **Run the script**:
   ```bash
   python 3.langraph.py
   ```

3. **Interact with the chatbot**:  
   - Type a message to get a response from the bot.  
   - To exit, enter `q`, `quit`, or `exit`.  

### 🛠️ Script Functionality

1. **Loads environment variables**.  
2. **Initializes the language model** `llama3.2:3b`.  
 ```bash
llm = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")
response = llm.invoke("tell me something about the sea in 5 lines")
   ```
![Alt text](assets/langraph_messages1.JPG)

**Response content:**
response->  The sea is a vast and mysterious body of saltwater that covers over 70% of the Earth's surface. It plays a crucial role in regulating the planet's climate and weather patterns. The sea also supports an incredible array of marine life, from tiny plankton to massive blue whales. Its depth ranges from just a few meters to over 11,000 meters in the Mariana Trench. The sea has been a source of inspiration for humans throughout history, influencing art, literature, and mythology.

3. **Defines the chatbot state** using `TypedDict`.  
State is a TypedDict that defines a chatbot's state. messages is a list processed using add_messages
Annotated[list, add_messages] is a hint that messages should be modified by add_messages.
 ```bash
class State(TypedDict):
    #{"message":"your message"}
    messages: Annotated[list, add_messages]
def chatbot(state: State):
    response = llm.invoke(state["messages"])  # Invoke the LLM with the current messages
    return {"messages": [response]}  # Return the response as part of the state
```
4. **Creates a state graph** with `LangGraph`:  
   - The chatbot processes messages and maintains conversation history.  
   - Responses are generated using `ChatOllama`.  
   graph_builder = StateGraph(State)
 ```bash
# Add a chatbot node to handle messages
graph_builder.add_node("chatbot", chatbot)
# Define edges (transitions) between different states # START --> chatbot --> END
graph_builder.add_edge(START, "chatbot")  # Start the conversation with the chatbot
graph_builder.add_edge("chatbot", END)  # End conversation after the chatbot responds
graph = graph_builder.compile() # Compile the graph
response=graph.invoke({"messages": ["tell me something about the sea in ten words"]})
```
![Alt text](assets/langraph_messages2.JPG)

5. **Visualizes the chatbot flow** by generating an image `langraph_flow.png`.  
6. **Runs a continuous chat loop** until the user decides to exit.  
```bash
while True:
    user_input = input("You: ")  # Get user input
    if user_input in ['q', 'quit', 'exit']:  # Exit condition
        print("Bye!")
        break
    
    response = graph.invoke({"messages": [user_input]})  # Process user input through the graph
    print("Assistant:", response["messages"][-1].content)  # Print the chatbot's response
```
### 📄 Example Usage

```text
You: Hello
Assistant: Hi! How can I help you?

You: Tell me something about the sea in 10 words
Assistant: The ocean covers more than 70% of the Earth's surface.

You: exit
Bye!
```

### 📷 Flow Visualization
The script generates an image `langraph_flow.png` representing the chatbot's structure in a state graph.

### 🏗️ Future Improvements
- Implement conversation history storage.  
- Integrate with an external API to enhance responses.  
- Add more nodes to the graph to handle different query types.  


## 3️⃣ Chatbot Langraph

This script sets up a chatbot using LangGraph, LangChain, and Ollama (a local LLM). The chatbot is capable of answering user queries either by using an LLM or by searching the web for real-time information.

Generate api key -> https://app.tavily.com/home 

![Alt text](assets/tool_explanation.JPG)


### Imports:
- TavilySearchResults: A tool for web search.
- ToolNode, tools_condition: Used to create and manage tools in LangGraph.
- HumanMessage, tool: Essential for LangChain's tool-based interactions.
- ChatOllama: A local LLM interface.
### Defining the LLM (ChatOllama):

- llm = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")
- This initializes the chatbot using the LLaMA 3.2 model running locally.
### Defining Tools:

- internet_search: Uses TavilySearchResults to fetch real-time web data.
- llm_search: Uses the LLM to generate responses from its trained knowledge.
### Binding Tools to LLM:
- The chatbot is configured to use either the LLM or the internet search tool based on the query.
### State and Memory Management:
- State: Stores messages exchanged in the conversation.
- MemorySaver(): Saves conversation history.
### Building the Graph-Based Chatbot:
- Nodes:
"chatbot": Handles conversation flow.
"tools": Executes the selected tool (either LLM or web search).
- Edges:
The chatbot node decides whether to use a tool.
The tool node processes the query and returns results to the chatbot.
### Visualization:
In LangGraph, when you define a StateGraph, you do not need to explicitly define the start and end nodes. The library automatically assigns these states based on the workflow structure.
![Alt text](assets/chatbot_langraph_flow.png)

### Example: Query the chatbot about Earth  
Tu información está estructurada como un diccionario que contiene una lista de mensajes en messages. Cada mensaje puede ser de tipo:
- HumanMessage → Mensaje del usuario
- AIMessage → Respuesta de la IA
- ToolMessage → Respuesta de una herramienta externa usada por la IA

### Running the Chatbot:
- The chatbot operates in a while True loop.
- The user can input queries, and responses are fetched using the graph-based chatbot.
- The program exits when the user types "exit", "quit", or "q".
### Summary
- This chatbot integrates LangGraph for structured interactions.
- It uses LLaMA 3.2 for AI-generated responses and TavilySearchResults for real-time web search.
- The chatbot decides whether to answer from its own knowledge or search the internet.
- It continuously interacts with users until they choose to exit.


### 4️⃣ Chatbot using LangGraph, LangChain, and Ollama


#### Overview
This script sets up a chatbot utilizing **LangGraph**, **LangChain**, and **Ollama** (a local LLM). The chatbot is capable of answering user queries either by using an LLM or by searching the web for real-time information.

#### Features
- **Local LLM (LLaMA 3.2)**: The chatbot can answer general queries using a locally hosted **LLaMA 3.2 model**.
- **Internet Search**: For real-time data such as news, stock trends, or weather, the chatbot can retrieve relevant web search results.
- **State Management**: Uses **LangGraph** for managing chatbot interactions.
- **Tool Integration**: LLM and web search tools are seamlessly integrated.
- **Interactive Mode**: Runs a chatbot loop that continuously accepts user input.

#### Requirements
To run this script, you need the following dependencies:
- **Python 3.8+**
- **LangGraph**
- **LangChain**
- **Ollama**
- **TavilySearch** (for real-time web search)

Install the dependencies using:
```bash
pip install langchain langgraph ollama tavily-search
```

#### Usage
##### 1. Start the chatbot
Run the script in a terminal:
```bash
python chatbot_langraph.py
```

##### 2. Query the chatbot
- Type a question, and the chatbot will respond based on the LLM or web search.
- To exit, type `exit`, `quit`, or `q`.

##### Example:
```
> Tell me about the earth in 3 points
1. The Earth is the third planet from the Sun.
2. It is the only known planet to support life.
3. About 71% of its surface is covered in water.
```

#### How It Works
1. **Initialize the LLM**: The script sets up **LLaMA 3.2** as the primary language model.
2. **Define Tools**:
   - `internet_search(query)`: Performs a web search to retrieve real-time information.
   - `llm_search(query)`: Uses the LLM to generate responses.
3. **State and Memory**:
   - Uses `LangGraph` to manage chatbot states and interactions.
   - Keeps track of conversation history with `MemorySaver`.
4. **LangGraph Workflow**:
   - The chatbot decides whether to use the LLM or perform a web search.
   - The interaction flow is managed using a state machine.
   - A **graph representation** of the workflow is generated (`chatbot_langraph_flow.png`).
5. **Interactive Chat Mode**:
   - Waits for user input.
   - Processes the input using `LangGraph`.
   - Outputs the response.
   - Continues until the user exits.

#### Future Enhancements
- Add support for multiple LLM models.
- Improve response accuracy with better search filtering.
- Implement a web-based interface.




### 
###
###
###