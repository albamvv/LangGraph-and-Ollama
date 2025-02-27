from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Acceder a las variables
api_key = os.getenv("LANGCHAIN_API_KEY")
endpoint = os.getenv("LANGCHAIN_ENDPOINT")
tracing = os.getenv("LANGSMITH_TRACING")

print(f"API Key: {api_key}")
print(f"Endpoint: {endpoint}")
print(f"Tracing: {tracing}")