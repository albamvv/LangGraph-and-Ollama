-   Documents loaders : https://python.langchain.com/docs/integrations/document_loaders/
-   PymuPDF : https://python.langchain.com/docs/integrations/document_loaders/pymupdf/


# Project 1: Question Answering from PDF Document


## 📌 Overview  
This script is designed for **Question Answering (QA) from PDF documents** using **LangChain** and **Ollama**.  
It loads PDFs, extracts text, and allows users to ask questions based on the extracted content.  



---

##  1. Loading a Single PDF File  
```python
loader = PyMuPDFLoader("rag-dataset/health supplements/1. dietary supplements - for whom.pdf")
docs = loader.load()
```
- `PyMuPDFLoader` loads a **specific** PDF file.  
- `.load()` extracts **text and metadata**, storing them in `docs`.  

---

## 2. Reading All PDFs from a Directory  
```python
pdfs = []
for root, dirs, files in os.walk("rag-dataset"):
    for file in files:
        if file.endswith(".pdf"):
            pdfs.append(os.path.join(root, file))
```
- This **scans** the `rag-dataset` directory for **all PDF files** and stores their file paths in `pdfs`.  

###  Example of `pdfs` List:  
```python
pdfs= [
    "rag-dataset/document1.pdf",
    "rag-dataset/supplements/report.pdf"
]
```

---

## 3. Loading and Storing Text from All PDFs  
```python
docs = []
for pdf in pdfs:
    loader = PyMuPDFLoader(pdf)
    temp = loader.load()
    docs.extend(temp)
```
- Iterates through **all PDFs**, loads their content, and **stores** the extracted text & metadata in `docs`.  

### Example Structure of `docs`:  
```python
[
    Document(page_content="Text from PDF 1...", metadata={'source': 'rag-dataset/doc1.pdf'}),
    Document(page_content="Text from PDF 2...", metadata={'source': 'rag-dataset/doc2.pdf'})
]
```

---

## 4. Formatting Extracted Documents  
```python
def format_docs(docs):
    return "\n\n".join([x.page_content for x in docs])

context = format_docs(docs)
```
- This function **combines all extracted text** from multiple PDFs into a single string (`context`).  

---

## 5. Tokenizing Text for GPT-4o-mini  
```python
encoding = tiktoken.encoding_for_model("gpt-4o-mini")
```
- Uses **OpenAI’s tokenizer** (`tiktoken`) to encode text before sending it to the AI model.  

###  Example Tokenization:  
```python
print(encoding.encode("congratulations"))  
# Output: [542, 111291, 14571]
```

---

##  6. Setting Up the LLM Model (Ollama)  
```python
base_url = "http://localhost:11434"
model = 'llama3.2:3b'
llm = ChatOllama(base_url=base_url, model=model)
```
- **Ollama’s LLaMA 3 model** is configured to answer user questions.  
- `base_url = "http://localhost:11434"` assumes **Ollama is running locally**.  

---

## 7. Defining the System Message (AI Behavior)  
```python
system = SystemMessagePromptTemplate.from_template("""
    You are a helpful AI assistant who answers user questions based on the provided context.
    Do not answer in more than {words} words.
""")
```
- **Instructs the AI** to answer **only using the provided PDF content**.  
- Limits responses to `{words}` words.  

---

## 8. Creating a Human Message Template  
```python
prompt = """Answer user question based on the provided context ONLY!
            If you do not know the answer, just say "I don't know".

            ### Context:
            {context}

            ### Question:
            {question}

            ### Answer:"""

prompt = HumanMessagePromptTemplate.from_template(prompt)
```
- Formats **user questions** and ensures the AI doesn’t generate responses **outside the given context**.  

---

## 9. Combining the AI Pipeline  
```python
messages = [system, prompt]
template = ChatPromptTemplate(messages)
```
- **Combines** system & user messages into a structured **prompt template**.  

---

## 10. Creating a Q&A Chain  
```python
qna_chain = template | llm | StrOutputParser()
```
- **Connects**:  
  1. **Prompt template** (`template`)  
  2. **LLM model** (`llm`)  
  3. **Output parser** (`StrOutputParser()`)  

---

## 11. Running Sample Questions  
```python
response = qna_chain.invoke({'context': context, 'question': "How to gain muscle mass?", 'words': 50})
print(response)
```
- Sends a **query** through the `qna_chain` and **prints** the AI’s response.  

### 💡 Other Sample Questions:  
```python
response = qna_chain.invoke({'context': context, 'question': "How to reduce weight?", 'words': 50})
print(response)

response = qna_chain.invoke({'context': context, 'question': "How many planets exist outside our solar system?", 'words': 50})
print(response)
```
- AI **answers based on extracted PDF content**.  

---

## 📊 Summary of Key Components  

| **Component** | **Purpose** |
|--------------|------------|
| `PyMuPDFLoader` | Extracts text from PDFs |
| `os.walk("rag-dataset")` | Finds all PDFs in a folder |
| `format_docs(docs)` | Formats extracted text for readability |
| `tiktoken.encoding_for_model("gpt-4o-mini")` | Tokenizes text for AI processing |
| `ChatOllama(base_url, model)` | Runs **LLaMA 3 model** for answering questions |
| `ChatPromptTemplate(messages)` | Combines system & user messages into a prompt template |
| `qna_chain.invoke(...)` | Runs the AI to answer user questions based on PDFs |

---

## ✅ Final Thoughts  
This script is **a complete PDF-based Question Answering system**. It:  
📄 **Extracts text from PDFs**  
🤖 **Uses a local AI model (Ollama) to answer questions**  
🔍 **Ensures responses stay within the given PDF content**  

Would you like help modifying or optimizing it further? 🚀


# Project 2: PDF Document Summarization


# Project 3: Report Generation from PDF Document