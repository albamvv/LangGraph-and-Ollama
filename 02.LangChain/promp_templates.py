
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama 

#-------------------- Langchain message ---------------------
base_url = "http://localhost:11434"
model = 'llama3.2:1b'

llm = ChatOllama(base_url=base_url, model=model)
question = HumanMessage('tell me about the earth in 3 points')
system = SystemMessage('You are elemetary teacher. You answer in short sentences.')

messages = [system, question]
response = llm.invoke(messages)

print("response-> ",response)
print(response.content)