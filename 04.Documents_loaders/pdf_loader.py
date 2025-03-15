from langchain_community.document_loaders import PyMuPDFLoader
import os


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