from langchain_ollama import ChatOllama 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import TavilySearchResults
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool

from dotenv import load_dotenv  # Used to load environment variables from a .env file
load_dotenv()

llm = ChatOllama(model='llama3.2:3b', base_url='http://localhost:11434')
#print(llm.invoke('hi').content)

### -------------------------------- Tool Creation ---------------------------------------

@tool
def add(a, b):
    """
    Add two integer numbers together
    
    Args:
    a: First Integer
    b: Second Integer
    """
    return a + b

@tool
def multiply(a, b):
    """
    Multiply two integer numbers together
    
    Args:
    a: First Integer
    b: Second Integer
    """
    return a * b

#print("atributos-> ",dir(add))  # Muestra todos los atributos disponibles en `add`
#print(add.name, add.description, add.args, add.args_schema.model_json_schema())

#print("suma-> ",add.invoke({'a': 1, 'b': 2}))
#print("multiplicacion->",multiply.invoke({'a': 67, 'b': 2}))

#tools es una lista que contiene las funciones add y multiply, que han sido decoradas con @tool.
#Esto significa que estas funciones son herramientas registradas y pueden ser llamadas por un agente de IA.
tools = [add, multiply]
#bind_tools(tools) asigna las herramientas al modelo llm.
#Ahora, el modelo puede llamar automáticamente estas funciones cuando sea necesario.
#Si llm es un modelo de LangChain (como OpenAI, Llama, etc.), esto le permite razonar sobre cuándo y cómo usar estas herramientas
llm_with_tools = llm.bind_tools(tools)

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
# There are so many other paid options are also available like Tavily, Google, Bing, etc.
# https://python.langchain.com/docs/integrations/tools/

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

@tool
def wikipedia_search(query):
    """
    Search wikipedia for general information.
    Args:
    query: The search query
    """
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    response = wikipedia.invoke(query)
    return response

@tool
def pubmed_search(query):
    """
    Search pubmed for medical and life sciences queries.
    Args:
    query: The search query
    """
    search = PubmedQueryRun()
    response = search.invoke(query)
    return response

@tool
def tavily_search(query):
    """
    Search the web for realtime and latest information.for examples, news, stock market, weather updates etc.
    Args:
    query: The search query
    """
    search = TavilySearchResults(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
    )
    response = search.invoke(query)
    return response
@tool
def multiply(a:int, b:int)->int:
    """
    Multiply two integer numbers together 
    Args:
    a: First Integer
    b: Second Integer
    """
    return int(a) * int(b)


# Define a list of tools, each representing a different search function or operation
tools = [wikipedia_search, pubmed_search, tavily_search, multiply]

# Create a dictionary where the keys are the tool names and the values are the tool objects
list_of_tools = {tool.name: tool for tool in tools}

# Output the dictionary containing the tools
#print("lista de herramientas->",list_of_tools)

# This code integrates an LLM (Large Language Model) with custom tools and processes a query to determine if any tool should be invoked.

# bind_tools(tools) links the model (llm) with the available tools (e.g., Wikipedia search, PubMed search, Tavily search, or a multiplication function).
# Now, the LLM can automatically decide whether a tool should be used to answer a query.
llm_with_tools = llm.bind_tools(tools)

#query = "What is the latest news"
# query = "What is today's stock market news?"
# query = "What is LLM?"
# query = "How to treat lung cancer?"
query  = "what is 2 * 3?"

'''
This sends the query to llm_with_tools, which:
- Processes the question.
- Determines if a tool is needed.
- Calls the appropriate tool (if necessary).
- Generates a response.
'''
response = llm_with_tools.invoke(query)
#print("estructura de la respuesta->", response.tool_calls)  # Muestra la estructura real

if response.tool_calls:
    selected_tool = response.tool_calls[0]['name']  # Acceder al nombre de la herramienta
    print(f"The selected tool is: {selected_tool}")
else:
    print("No tool was selected.")



#----------------------------- Generate Final Result with Tool Calling --------------------------------

# query = "What is the latest news"
# query = "What is today's stock market news?"
# query = "What is LLM?"
# query = "How to treat lung cancer?"
query = "what is 2 * 3?"

# Create a list of messages with the user's query as a HumanMessage
messages = [HumanMessage(query)]

# Invoke the LLM with tools using the provided messages
tool_calls_response = llm_with_tools.invoke(messages)
#print("tool calls-> ",tool_calls)
# tool calls->  content='' additional_kwargs={} response_metadata={'model': 'llama3.2:3b', 'created_at': '2025-03-03T12:03:10.4621722Z', 'done': True, 'done_reason': 'stop', 'total_duration': 3589878600, 'load_duration': 66508700, 'prompt_eval_count': 357, 'prompt_eval_duration': 129000000, 'eval_count': 22, 'eval_duration': 3392000000, 'message': Message(role='assistant', content='', images=None, tool_calls=None)} id='run-1da51719-1f35-4922-bf0b-aeeeec6b91f2-0' 
# tool_calls=[{'name': 'multiply', 'args': {'a': 2, 'b': 3}, 'id': '74fdaf4b-6710-46bf-a1eb-fc3d3e6afc55', 'type': 'tool_call'}] usage_metadata={'input_tokens': 357, 'output_tokens': 22, 'total_tokens': 379}

# Append the tool_calls response to the message list
messages.append(tool_calls_response)
#print("messages-> ",messages)

# Extract the tool calls from the response for further processing
tool_calls = tool_calls_response.tool_calls
#print('tool_calls-> ',tool_calls)
#tool_calls->  [{'name': 'multiply', 'args': {'a': 2, 'b': 3}, 'id': 'e2425e61-21e7-4cb8-a2b1-ef831cb42cf3', 'type': 'tool_call'}]

# ---------------------------------------------------------------------
query = "What is medicine for lung cancer?"
# Se guarda la pregunta en una lista messages, representada como un HumanMessage.
messages = [HumanMessage(query)]
print('messages->',messages)
#print('------------------')
#messages-> [HumanMessage(content='What is medicine for lung cancer?', additional_kwargs={}, response_metadata={})]
ai_msg = llm_with_tools.invoke(messages) # LLM processes the query
#print("ai_msg-> ",ai_msg)
#ai_msg->  content='' additional_kwargs={} response_metadata={'model': 'llama3.2:3b', 'created_at': '2025-03-03T12:33:58.9114827Z', 'done': True, 'done_reason': 'stop', 'total_duration': 3828343600, 'load_duration': 55061300, 'prompt_eval_count': 356, 'prompt_eval_duration': 977000000, 'eval_count': 21, 'eval_duration': 2792000000, 'message': Message(role='assistant', content='', images=None, tool_calls=None)} id='run-25dec1fb-f784-4250-8416-2e04cdd65280-0' 
#tool_calls=[{'name': 'pubmed_search', 'args': {'query': 'medicine for lung cancer'}, 'id': 'a48172e0-3ec6-4ab8-89e9-0853d3ce9a97', 'type': 'tool_call'}] usage_metadata={'input_tokens': 356, 'output_tokens': 21, 'total_tokens': 377}
messages.append(ai_msg) # Append AI's response to the messages
#print("messages-> ",type(messages))



for tool_call in ai_msg.tool_calls:
    #print("tool call->", tool_call)
    name = tool_call['name'].lower()  # Get the tool name
    selected_tool = list_of_tools[name]  # Find the tool from the dictionary
    tool_msg = selected_tool.invoke(tool_call)  # Execute the tool
    messages.append(tool_msg)  # Append the tool response
#print("---------------------------")
#print("messages-> ",messages)
      
# Se vuelve a invocar al LLM con la nueva información
response = llm_with_tools.invoke(messages)
#print("Response->" ,response.content)