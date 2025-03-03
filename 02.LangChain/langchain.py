# Import necessary libraries
from dotenv import load_dotenv  # Used to load environment variables from a .env file
from langchain_ollama import ChatOllama  # LangChain integration for Ollama models
import os  # Provides functions to interact with the operating system

# Load environment variables from the .env file
load_dotenv()

# Retrieve environment variables (not used in this script)
api_key = os.getenv("LANGCHAIN_API_KEY")  # API key for LangChain (if needed)
endpoint = os.getenv("LANGCHAIN_ENDPOINT")  # Endpoint URL for LangChain API (if needed)
tracing = os.getenv("LANGSMITH_TRACING")  # Tracing option for debugging (if needed)

# Define the base URL for the local Ollama server
base_url = "http://localhost:11434"

# Specify the language model to use
model = 'llama3.2:1b'

'''
Reference to the ChatOllama documentation:
https://python.langchain.com/api_reference/ollama/chat_models/langchain_ollama.chat_models.ChatOllama.html#langchain_ollama.chat_models.ChatOllama
'''

# Initialize the Ollama-based language model (LLM) with specific parameters
llm = ChatOllama(
    base_url=base_url,  # The URL where the Ollama server is running
    model=model,  # The specific LLaMA model being used
    temperature=0.8,  # Controls response randomness (higher value = more creative)
    num_predict=256,  # Limits the response to 256 tokens
    # Additional parameters can be added here...
)

# Debugging: Print the LLM object (commented out)
# print("llm-> ", llm)

# Define the input sentence (query) for the model
sentence = "hi"  # First test input (English)
sentence = "¿Cuáles son las causas y consecuencias del cambio climático?"  # Spanish query

# Invoke the model with the given sentence and store the response
response = llm.invoke(sentence)

# Print the model's response to the console
#print(response.content)

#print("metadata-> ",response.response_metadata)

'''
response = ""
for chunk in llm.stream('¿Cuáles son las causas y consecuencias del cambio climático?. Responde en 5 frases'):
    response = response + " " + chunk.content
    print(response)
'''

