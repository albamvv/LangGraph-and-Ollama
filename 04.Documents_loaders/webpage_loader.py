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
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks