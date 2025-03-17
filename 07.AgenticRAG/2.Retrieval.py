from imports import*

embeddings = OllamaEmbeddings(model='nomic-embed-text', base_url='http://localhost:11434')

db_name = r"D:\NLP\LLM\Langchain and Ollama\09. Vector Stores and Retrievals\health_supplements"
vector_store = FAISS.load_local(db_name, embeddings, allow_dangerous_deserialization=True)


### Retreival
question = "how to gain muscle mass?"
docs = vector_store.search(query=question, k=5, search_type="similarity")
print(docs)
retriever = vector_store.as_retriever(search_type = 'similarity', 
                                      search_kwargs = {'k': 3})

retriever.invoke(question)

question = "how to lose weight?"
retriever.invoke(question)

retriever = vector_store.as_retriever(search_type = 'similarity_score_threshold', 
                                      search_kwargs = {'k': 3, 'score_threshold': 0.1})

retriever.invoke(question)

retriever = vector_store.as_retriever(search_type = 'mmr', 
                                      search_kwargs = {'k': 3, 'fetch_k': 20, 'lambda_mult': 1})

docs = retriever.invoke(question)
docs