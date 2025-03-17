from imports import*
from config import embeddings,db_name, vector_store


### Retreival
question = "how to gain muscle mass?"
# This line performs a search in the vector_store to find documents that are most similar to the provided question.
docs = vector_store.search(query=question, k=5, search_type="similarity")
# This line creates a retriever object from the vector_store. The retriever is responsible for fetching relevant documents based on a query.
retriever = vector_store.as_retriever(search_type = 'similarity', search_kwargs = {'k': 3})
response=retriever.invoke(question)
#--------------------------------
question = "how to lose weight?"
response=retriever.invoke(question)
#--------------------------------
retriever = vector_store.as_retriever(search_type = 'similarity_score_threshold', search_kwargs = {'k': 3, 'score_threshold': 0.1})
response= retriever.invoke(question)
#--------------------------------
retriever = vector_store.as_retriever(search_type = 'mmr', search_kwargs = {'k': 3, 'fetch_k': 20, 'lambda_mult': 1})
response = retriever.invoke(question)


for doc in response:
    print(f"📄 Source: {doc.metadata['source']} (Page {doc.metadata['page']})")
    print(f"📌 Content: {doc.page_content}\n")