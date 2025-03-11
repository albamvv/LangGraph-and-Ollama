from imports import*
from config import llm, embeddings,db_name



# -------------------- Retriever ------------------------

vector_store = FAISS.load_local(db_name, embeddings, allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs = {'k': 5})
question = "how to gain muscle mass?"
response=retriever.invoke(question)
'''
for doc in response:
    print(f"📄 Source: {doc.metadata['source']} (Page {doc.metadata['page']})")
    print(f"📌 Content: {doc.page_content}\n")

'''

retriever_tool = create_retriever_tool(
    retriever,
    "health_supplements", # tool name
    "Search and return information about the Health Supplements for workout and gym",
)

tools = [retriever_tool]
print("tools-> ",tools)
