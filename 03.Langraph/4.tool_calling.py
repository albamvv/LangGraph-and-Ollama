from imports import *
from utils import add,multiply,multiply2,wikipedia_search, pubmed_search, tavily_search
from constant import query1,query2,query3,query4,query5

load_dotenv()
llm = ChatOllama(model='llama3.2:3b', base_url='http://localhost:11434')

### -------------------------------- Tool Creation ---------------------------------------

#print("atributos-> ",dir(add))  # Muestra todos los atributos disponibles en `add`
#print(add.name, add.description, add.args, add.args_schema.model_json_schema())
#print("suma-> ",add.invoke({'a': 1, 'b': 2}))
#print("multiplicacion->",multiply.invoke({'a': 67, 'b': 2}))

# Lista que contiene las funciones add y multiply, que han sido decoradas con @tool.
tools = [add, multiply] #Ahora, el modelo puede llamar automáticamente estas funciones cuando sea necesario.
llm_with_tools = llm.bind_tools(tools) #bind_tools(tools) asigna las herramientas al modelo llm.

question  = "what is 1 plus 2?"
tool_response=llm_with_tools.invoke(question).tool_calls
#print("tool_response-> ",tool_response) 
# tool_response->  [{'name': 'add', 'args': {'a': 1, 'b': 2}, 'id': '52877c2b-27d1-45f7-aeff-dd62ce2b8cef', 'type': 'tool_call'}]
question  = "what is 1 multiplied by 2?"
tool_response2=llm_with_tools.invoke(question).tool_calls
#print("tool_response2-> ",tool_response2)
# tool_response2->  [{'name': 'multiply', 'args': {'a': 1, 'b': 2}, 'id': '33954844-e730-4a21-a9a3-f381e0e9f6d0', 'type': 'tool_call'}]
question  = "what is 1 multiplied by 2, also what is 11 plus 22?"
tool_response3=llm_with_tools.invoke(question).tool_calls
#print("tool_response3-> ",tool_response3)
# tool_response3->  [{'name': 'multiply', 'args': {'a': 1, 'b': 2}, 'id': '8df07d15-a565-43c7-b593-3b51354287aa', 'type': 'tool_call'},
# {'name': 'add', 'args': {'a': 11, 'b': 22}, 'id': 'cd800eca-b2fb-4db2-8086-8b24a20e6c61', 'type': 'tool_call'}]


#-------------------------------------------- Calling In-Built Tool --------------------------------------------

# DuckDuckGo Search
# Crea una instancia de DuckDuckGoSearchRun, que es una clase utilizada en LangChain para ejecutar búsquedas en DuckDuckGo.
search = DuckDuckGoSearchRun()
#print(search.invoke("What is today's stock market news?"))

# Tavily search
search = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
)
question = "what is today's stock market news?"
#print(search.invoke(question))

# Wikipedia
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
question = "what is the capital of France?"
question = "What is LLM?"
#print(wikipedia.invoke(question))

# -------------------------------------- Tool Calling with LLM -------------------------------------

# Define a list of tools, each representing a different search function or operation
tools = [wikipedia_search, pubmed_search, tavily_search, multiply2]
list_of_tools = {tool.name: tool for tool in tools} 
# This code integrates an LLM with custom tools and processes a query to determine if any tool should be invoked.
llm_with_tools = llm.bind_tools(tools)
#Calls the appropriate tool (if necessary).Generates a response.
tool_calls_response = llm_with_tools.invoke(query5)
#print("estructura de la respuesta->", response.tool_calls)  # Muestra la estructura real

if tool_calls_response.tool_calls:
    selected_tool = tool_calls_response.tool_calls[0]['name']  # Acceder al nombre de la herramienta
    print(f"The selected tool is: {selected_tool}")
else:
    print("No tool was selected.")

#----------------------------- Generate Final Result with Tool Calling --------------------------------

# Create a list of messages with the user's query as a HumanMessage
messages = [HumanMessage(query5)] 
tool_calls_response = llm_with_tools.invoke(messages) 
print("tool_calls_response",tool_calls_response)
messages.append(tool_calls_response) # Append the tool_calls response to the message list
tool_calls = tool_calls_response.tool_calls # Extract the tool calls from the response for further processing

# ---------------------------------------------------------------------

messages = [HumanMessage(query4)]
ai_msg = llm_with_tools.invoke(messages) # AIMessage representa la respuesta del modelo, que puede incluir una llamada a herramientas.
print('ai_msg',ai_msg)
messages.append(ai_msg) # Append AI's response to the messages

for tool_call in ai_msg.tool_calls:
    #print("tool call->", tool_call)
    name = tool_call['name'].lower()  # Get the tool name
    selected_tool = list_of_tools[name]  # Find the tool from the dictionary
    # ToolMessage representa la respuesta de la herramienta después de ser ejecutada.
    tool_msg = selected_tool.invoke(tool_call)  # Execute the tool
    messages.append(tool_msg)  # Append the tool response
#("messages-> ",messages)
      
# Se vuelve a invocar al LLM con la nueva información
response = llm_with_tools.invoke(messages)
print("Response->" ,response.content)