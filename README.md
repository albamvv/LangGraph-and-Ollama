# LangGraph-and-Ollama

https://pytorch.org/get-started/locally/

## 1️⃣ Langchain getting started

This Python code sets up and uses the LangChain Ollama library to interact with a local instance of the LLaMA 3.2 (1B) model for generating responses to user queries. Here's a breakdown of what it does:

### Import necessary libraries:

- dotenv is used to load environment variables from a .env file.
- os is used to access these environment variables.
- ChatOllama from langchain_ollama is used to communicate with the Ollama language model.

### Load environment variables:

- The load_dotenv() function loads variables from a .env file.
- Variables such as LANGCHAIN_API_KEY, LANGCHAIN_ENDPOINT, and LANGSMITH_TRACING are retrieved using os.getenv(), but they are not used in the code.

### Set up the model parameters:

- The local server URL for Ollama is defined as http://localhost:11434.
- The specific LLaMA model used is "llama3.2:1b".
- A link to LangChain's documentation for ChatOllama is included as a comment.

### Initialize the language model (llm):

- The ChatOllama class is instantiated with:
base_url: The URL where the Ollama server is running.
model: The specific LLaMA model version.
temperature: Set to 0.8, meaning responses will have a moderate level of randomness.
num_predict: Limited to 256 tokens for response generation.
Other parameters (not explicitly defined in the code).
 ### Generate a response from the model:

- A Spanish sentence, "¿Cuáles son las causas y consecuencias del cambio climático?", is assigned to sentence.
- The model is invoked with llm.invoke(sentence), generating a response.
- The response content is printed to the console.
### Key Takeaways:
- The script connects to a locally hosted Ollama instance.
- It uses the LLaMA 3.2 (1B) model to process and respond to queries.
- The .env variables are loaded but not actively used in the script.
- The temperature and token limit settings control the model’s response style and length.