from imports import*
from config import embeddings,db_name, vector_store,llm
from utils import health_supplements, search

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
load_dotenv()

retriever = vector_store.as_retriever(search_type = 'similarity', 
                                      search_kwargs = {'k': 3})
@tool
def health_supplements(query: str) -> str:
    """Search for information about Health Supplements.
    For any questions about Health and Gym Supplements, you must use this tool!,

    Args:
        query: The search query.
    """
    response = retriever.invoke(query)
    return response
response=health_supplements.invoke("what is the best supplement for muscle gain?")
'''
for doc in response:
    print(f"📄 Source: {doc.metadata['source']} (Page {doc.metadata['page']})")
    print(f"📌 Content: {doc.page_content}\n")
'''

# ----------------- Agent -------------
prompt = hub.pull("hwchase17/openai-functions-agent")
#pprint(prompt.messages, indent=2, width=80)
# https://smith.langchain.com/hub

tools = [search, health_supplements]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
#question = "What is the best supplement for muscle gain?"
#question = "what's weather in New York?"
question = "What are the side effects of taking too much vitamin D?"
response = agent_executor.invoke({'input': question})