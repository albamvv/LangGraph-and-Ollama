from imports import*
#-------------------- Simple chain -------------------
base_url = "http://localhost:11434"
model = 'llama3.2:3b'

llm = ChatOllama(base_url=base_url, model=model)

template = ChatPromptTemplate.from_template("{prompt}")
chain = template | llm | StrOutputParser()

about = "My name is Laxmi Kant. I work for KGP Talkie."
chain.invoke({'prompt': about})
#------------------------
prompt = "What is my name?"
chain.invoke({'prompt': prompt})