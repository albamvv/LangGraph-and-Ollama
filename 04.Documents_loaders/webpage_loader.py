from langchain_community.document_loaders import WebBaseLoader

urls = ['https://economictimes.indiatimes.com/markets/stocks/news',
        'https://www.livemint.com/latest-news',
        'https://www.livemint.com/latest-news/page-2'
        'https://www.livemint.com/latest-news/page-3',
        'https://www.moneycontrol.com/']

loader = WebBaseLoader(web_paths=urls)
docs = []
'''
async for doc in loader.alazy_load():
    docs.append(doc)
def format_docs(docs):
    return "\n\n".join([x.page_content for x in docs])
context = format_docs(docs)'
'''