from langchain_community.document_loaders import PyMuPDFLoader

loader = PyMuPDFLoader("rag-dataset/health supplements/1. dietary supplements - for whom.pdf")

docs = loader.load()
len(docs)

docs[0].metadata
print(docs[0].page_content)