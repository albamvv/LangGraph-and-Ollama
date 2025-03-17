from imports import*
from config import embeddings,db_name, vector_store,llm
from utils import health_supplements, search

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
load_dotenv()

# ----------------- Health Supplements Retriever -------------
query= "what is the best supplement for muscle gain?"
retriever = vector_store.as_retriever(search_type = 'similarity',  search_kwargs = {'k': 3})
response = health_supplements(query, retriever)

# ----------------- Agent -------------
prompt = hub.pull("hwchase17/openai-functions-agent")
pprint(prompt.messages, indent=2, width=80)
# https://smith.langchain.com/hub

tools = [search, health_supplements]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# question = "What is the best supplement for muscle gain?"
# question = "what's weather in New York?"
question = "What are the side effects of taking too much vitamin D?"
response = agent_executor.invoke({'input': question})