from imports import*

urls = ['https://economictimes.indiatimes.com/markets/stocks/news',
        'https://www.livemint.com/latest-news',
        'https://www.livemint.com/latest-news/page-2'
        'https://www.livemint.com/latest-news/page-3',
        'https://www.moneycontrol.com/']

loader = WebBaseLoader(web_paths=urls)

docs = []
async def load_documents():
    async for doc in loader.alazy_load():
        docs.append(doc)

asyncio.run(load_documents())  # Run the async function

def format_docs(docs):
    return "\n\n".join([x.page_content for x in docs])
context = format_docs(docs)

def text_clean(text):
    text = re.sub(r'\n\n+', '\n\n', text)
    text = re.sub(r'\t+', '\t', text)
    text = re.sub(r'\s+', ' ', text)
    return text
context = text_clean(context)
#print(context)


# Stock Market Data Processing with LLM
response = llm.ask_llm(context, "Extract stock market news from the given text.")
#print("response-> ",response)
response = llm.ask_llm(context[:10_000], "Extract stock market news from the given text.")
#print("response-> ",response)


def chunk_text(text, chunk_size, overlap=100):
    chunks = []  # List to store the chunks of text
    for i in range(0, len(text), chunk_size - overlap):  
        # Loop through the text in steps of (chunk_size - overlap)
        chunks.append(text[i:i + chunk_size])  
        # Take a substring from index 'i' to 'i + chunk_size' and add it to the chunks list
    return chunks  # Return the list of chunks


text = "This is an example of text that will be split into chunks."
chunks = chunk_text(text, chunk_size=10, overlap=3)
#print(chunks) # ['This is an', ' an exampl', 'mple of te', ' text that', 'hat will b', 'l be split', 'lit into c', 'o chunks.', 's.']

chunks = chunk_text(context, 10_000)
question = "Extract stock market news from the given text."

chunk_summary = []
for chunk in chunks:
    response = llm.ask_llm(chunk, question)
    chunk_summary.append(response)

for chunk in chunk_summary:
    print(chunk)
    print("\n\n")
    break
print("chunk_summary-> ",chunk_summary)


summary = "\n\n".join(chunk_summary)
# print(summary)
# question = "Write a detailed report in Markdown from the given context."
question = """Write a detailed market news report in markdown format. Think carefully then write the report."""
response = llm.ask_llm(summary, question)
import os

os.makedirs("data", exist_ok=True)

with open("data/report.md", "w") as f:
    f.write(response)
with open("data/summary.md", "w") as f:
    f.write(summary)