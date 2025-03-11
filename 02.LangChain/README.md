# Prompt template

![Alt text](assets/prompt_template.JPG)
# LangChain

## Overview
This Python script integrates with the **LangChain** framework using **Ollama** to process natural language queries. It initializes a local **Ollama** language model (LLaMA 3.2) and generates responses to user-provided queries.
- https://pytorch.org/get-started/locally/
- Reference to the ChatOllama documentation:
https://python.langchain.com/api_reference/ollama/chat_models/langchain_ollama.chat_models.ChatOllama.html#langchain_ollama.chat_models.ChatOllama

## Requirements
Ensure you have the following dependencies installed before running the script:

- Python 3.x
- `langchain_ollama` (LangChain integration for Ollama models)
- `dotenv` (For loading environment variables)
- An **Ollama** server running locally

## Installation
1. Clone the repository or copy the script to your local machine.
2. Install the required Python packages:
   ```sh
   pip install langchain_ollama python-dotenv
   ```
3. Set up an `.env` file in the same directory (if needed) with the following optional environment variables:
   ```ini
   LANGCHAIN_API_KEY=your_api_key_here
   LANGCHAIN_ENDPOINT=your_endpoint_here
   LANGSMITH_TRACING=false
   ```
4. Ensure the **Ollama** server is running locally at `http://localhost:11434`.

## Usage
Run the script using:
```sh
python langchain.py
```

The script sends the query:
```
"What are the causes and consequences of climate change?"
```
to the language model and prints the response.

## Configuration
The following parameters are defined in the script:
- **Model**: `llama3.2:1b`
- **Temperature**: `0.8` (Controls randomness; higher values generate more creative responses)
- **Response Length**: Limited to `256` tokens

To modify the query, update the `sentence` variable in the script.


### Notes
- Ensure that the **Ollama** server is running before executing the script.
- Modify the base URL, model, and parameters as needed for different configurations.

## Implementation

**1. Initialize the language model (llm):**

- **The ChatOllama class is instantiated with:**
  
```python
# Define the base URL for the local Ollama server
base_url = "http://localhost:11434"
# Specify the language model to use
model = 'llama3.2:1b'

# Initialize the Ollama-based language model (LLM) with specific parameters
llm = ChatOllama(
    base_url=base_url,  # The URL where the Ollama server is running
    model=model,  # The specific LLaMA model being used
    temperature=0.8,  # Controls response randomness (higher value = more creative)
    num_predict=256,  # Limits the response to 256 tokens
    # Additional parameters can be added here...
)
print("llm-> ", llm)
```
**Output:**
```bash 
llm->  model='llama3.2:1b' num_predict=256 temperature=0.8 base_url='http://localhost:11434'
```


**2. Generate a response from the model:**

- A query is assigned to sentence.
- The model is invoked with llm.invoke(sentence), generating a response.
- The response content is printed to the console.
```bash 
# Define the input sentence (query) for the model
sentence = "¿Cuáles son las causas y consecuencias del cambio climático?" 
# Invoke the model with the given sentence and store the response
response = llm.invoke(sentence)
# Print the model's response to the console
print(response.content)
```
## Key Takeaways:
- The script connects to a locally hosted Ollama instance.
- It uses the LLaMA 3.2 (1B) model to process and respond to queries.
- The .env variables are loaded but not actively used in the script.
- The temperature and token limit settings control the model’s response style and length.

