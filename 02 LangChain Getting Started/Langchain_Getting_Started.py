from dotenv import load_dotenv
from langchain_ollama import ChatOllama
import os

# Cargar variables del archivo .env
load_dotenv()

# Acceder a las variables
api_key = os.getenv("LANGCHAIN_API_KEY")
endpoint = os.getenv("LANGCHAIN_ENDPOINT")
tracing = os.getenv("LANGSMITH_TRACING")

#print(f"API Key: {api_key}")
#print(f"Endpoint: {endpoint}")
#print(f"Tracing: {tracing}")


base_url = "http://localhost:11434"
model = 'llama3.2:1b'

'''
https://python.langchain.com/api_reference/ollama/chat_models/langchain_ollama.chat_models.ChatOllama.html#langchain_ollama.chat_models.ChatOllama
'''

llm = ChatOllama(
    base_url=base_url,
    model = model,
    temperature = 0.8,
    num_predict = 256,
    # other params ...
)

#print("llm-> ",llm)

sentence ="hi"
sentence= "¿Cuáles son las causas y consecuencias del cambio climático?"
response = llm.invoke(sentence)
print(response.content)
