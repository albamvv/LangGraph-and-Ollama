from imports import*


#-------------------- Langchain message ---------------------
base_url = "http://localhost:11434"
model = 'llama3.2:1b'
#model = 'sherlock'
#model = 'sheldon'

llm = ChatOllama(base_url=base_url, model=model)
question = HumanMessage('tell me about the earth in 3 points')
system = SystemMessage('You are elemetary teacher. You answer in short sentences.')
#system = SystemMessage('You are phd teacher. You answer in short sentences.')

messages = [system, question]
response = llm.invoke(messages)

#print("response-> ",response)
#print(response.content)

#---------------------------- Langchain Prompt Templates----------------------


system = SystemMessagePromptTemplate.from_template('You are {school} teacher. You answer in short sentences.')
question = HumanMessagePromptTemplate.from_template('tell me about the {topics} in {points} points')
#print("system-> ",system)
#print("question-> ",question)

#print(question.format(topics='sun', points=5))
#print(system.format(school='elemetary'))

messages = [system, question]
template = ChatPromptTemplate(messages)
question = template.invoke({'school': 'elementary', 'topics': 'sun', 'points': 5})
response = llm.invoke(question)
print(response.content)