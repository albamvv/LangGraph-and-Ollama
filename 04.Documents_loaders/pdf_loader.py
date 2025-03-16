from imports import*

#Project 1: Question Answering from PDF Document

loader = PyMuPDFLoader("rag-dataset/health supplements/1. dietary supplements - for whom.pdf")

docs = loader.load()
#print("docs->", docs[0])
#print(docs[0].__dict__)
#print("doc metadata -> ",docs[0].metadata)
#print(docs[0].page_content)

### Read the list of PDFs in the dir
pdfs = []
for root, dirs, files in os.walk("rag-dataset"):
    # print(root, dirs, files)
    for file in files:
        if file.endswith(".pdf"):
            pdfs.append(os.path.join(root, file))
'''
pdfs= [
    "rag-dataset/document1.pdf",
    "rag-dataset/supplements/report.pdf"
]git 
'''
docs = []
for pdf in pdfs:
    loader = PyMuPDFLoader(pdf)
    temp = loader.load()
    docs.extend(temp)
    #print(temp)
    #break

'''
[
    Document(page_content="Texto del PDF 1...", metadata={'source': 'rag-dataset/doc1.pdf'}),
    Document(page_content="Texto del PDF 2...", metadata={'source': 'rag-dataset/doc2.pdf'})
]
'''

def format_docs(docs):
    return "\n\n".join([x.page_content for x in docs])
context = format_docs(docs)
#print(docs[0])

# This snippet uses the tiktoken library (OpenAI’s official tokenizer) to encode words into token sequences based on the gpt-4o-mini model.
encoding = tiktoken.encoding_for_model("gpt-4o-mini")
#print("encode1-> ",encoding.encode("congratulations")) # encode1->  [542, 111291, 14571]
#print("encode2-> ", encoding.encode("rqsqeft")) # encode2->  [81, 31847, 80, 5276]


base_url = "http://localhost:11434"
model = 'llama3.2:3b'
llm = ChatOllama(base_url=base_url, model=model)

system = SystemMessagePromptTemplate.from_template("""You are helpful AI assistant who answer user question based on the provided context. 
                                                    Do not answer in more than {words} words""")

prompt = """Answer user question based on the provided context ONLY! If you do not know the answer, just say "I don't know".
            ### Context:
            {context}

            ### Question:
            {question}

            ### Answer:"""

prompt = HumanMessagePromptTemplate.from_template(prompt)

messages = [system, prompt]
template = ChatPromptTemplate(messages)

# template
# template.invoke({'context': context, 'question': "How to gain muscle mass?", 'words': 50})

qna_chain = template | llm | StrOutputParser()
print("qna chain-> ",qna_chain)
response = qna_chain.invoke({'context': context, 'question': "How to gain muscle mass?", 'words': 50})
print(response)

response = qna_chain.invoke({'context': context, 'question': "How to reduce the weight?", 'words': 50})
print(response)

response = qna_chain.invoke({'context': context, 'question': "How to do weight loss?", 'words': 50})
print(response)

response = qna_chain.invoke({'context': context, 'question': "How many planets are there outside of our solar system?", 'words': 50})
print(response)


# Project 2: PDF Document Summarization

# Project 3: Report Generation from PDF Document

response = qna_chain.invoke({'context': context, 
                             'question': "Provide a detailed report from the provided context. Write answer in Markdown.", 
                             'words': 2000})
#print(response)