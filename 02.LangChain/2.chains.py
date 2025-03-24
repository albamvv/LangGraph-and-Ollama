from imports import*

# -----------------------  Sequential LCEL Chain -------------

base_url = "http://localhost:11434"
model = 'llama3.2:1b'
llm = ChatOllama(base_url=base_url, model=model)

system = SystemMessagePromptTemplate.from_template('You are {school} teacher. You answer in short sentences.')
question = HumanMessagePromptTemplate.from_template('tell me about the {topics} in {points} points')
messages = [system, question]
template = ChatPromptTemplate(messages)

#------- Example without chain ---------------------------------
question = template.invoke({'school': 'primary', 'topics': 'solar system', 'points': 5})
response1 = llm.invoke(question)
#print("response1-> ",response1.content)   

#---------Example with chain ----------------------------------------
chain = template | llm
#print("chain-> ",chain)
response2 = chain.invoke({'school': 'primary', 'topics': 'solar system', 'points': 5})
#print("response2-> ",response2.content)

#-------- Using StrOutParser ---------------------------------------
chain = template | llm | StrOutputParser()
response3 = chain.invoke({'school': 'primary', 'topics': 'solar system', 'points': 5})
#print("response3-> ",response3)


#-------------------------- Chaining Runnables (Chain Multiple Runnables)

analysis_prompt = ChatPromptTemplate.from_template('''analyze the following text: {response}
                                                   You need tell me that how difficult it is to understand.
                                                   Answer in one sentence only.
                                                   ''')

fact_check_chain = analysis_prompt | llm | StrOutputParser()
output = fact_check_chain.invoke({'response': response3})
#print(output)