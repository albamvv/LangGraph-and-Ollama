from imports import*
from config import embeddings,db_name, vector_store
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
load_dotenv()

# ----------------- Health Supplements Retriever -------------
query= "what is the best supplement for muscle gain?"
retriever = vector_store.as_retriever(search_type = 'similarity',  search_kwargs = {'k': 3})
response = retriever.invoke(query)


# ----------------- Agent -------------
prompt = hub.pull("hwchase17/openai-functions-agent")