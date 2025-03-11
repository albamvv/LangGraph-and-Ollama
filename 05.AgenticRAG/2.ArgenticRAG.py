from imports import*
from config import llm, embeddings,db_name



# -------------------- Retriever ------------------------

vector_store = FAISS.load_local(db_name, embeddings, allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs = {'k': 5})
question = "how to gain muscle mass?"
response=retriever.invoke(question)
print(response)

'''


retriever_tool = create_retriever_tool(
    retriever,
    "health_supplements",
    "Search and retrun information about the Health Supplements for workout and gym",
)

tools = [retriever_tool]'
'''