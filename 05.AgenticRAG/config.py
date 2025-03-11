from imports import*

model = "llama3.2:3b"
llm = ChatOllama(model=model, base_url="http://localhost:11434")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url='http://localhost:11434'
)

# Name of the database where the vectors will be stored
db_name = "health_supplements"