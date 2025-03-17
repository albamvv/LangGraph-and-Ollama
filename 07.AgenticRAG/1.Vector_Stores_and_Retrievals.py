from imports import*
from config import embeddings, db_name
from utils import load_pdfs_from_directory

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
warnings.filterwarnings("ignore")

load_dotenv()

loader = PyMuPDFLoader(r"rag-dataset\gym supplements\1. Analysis of Actual Fitness Supplement.pdf")
loader.load()

#-------------------------  Document Loader --------------------------
docs = load_pdfs_from_directory("rag-dataset")
#print(f"Total documents loaded: {len(docs)}")
#print(docs[0].page_content)

#------------------------------------ DOCUMENT CHUNKING -------------------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(docs)
#print(chunks[0].page_content)
#print("Atributos-> ",dir(chunks[0]))  # Muestra todos los atributos y métodos disponibles
#print("chunks metadata->", json.dumps(chunks[0].metadata, indent=4, ensure_ascii=False))
#len(chunks[0].page_content)
#chunks[150].metadata


#-------------------------------Document Vector Embedding --------------------------
#vector = embeddings.embed_query("Hello World")
vector = embeddings.embed_query(chunks[0].page_content)
#print("len vector-> ",len(vector))

# ----------------------------- Storing embedding in a vector -----------------------

# Create an IndexFlatIP (Inner Product) index for FAISS.
index = faiss.IndexFlatIP(len(vector))

# Check the total number of vectors currently stored in the index and the dimensionality (d) of the vectors.
# 'ntotal' refers to the total number of vectors in the index.
# 'd' refers to the dimensionality of the vectors in the index.
index.ntotal, index.d

# Initialize a FAISS vector store with the following parameters:
vector_store = FAISS(
    embedding_function=embeddings,      # The embedding function to use for document embeddings.
    index=index,                        # The FAISS index where embeddings will be added.
    docstore=InMemoryDocstore(),        # The in-memory document store to hold the documents.
    index_to_docstore_id={}            # Mapping from FAISS index IDs to document store IDs (empty initially).
)

# After initializing, we check how many vectors are currently in the index by accessing 'ntotal' of the FAISS index.
num_samples=vector_store.index.ntotal

# Add documents (in chunks) to the vector store.
# This adds the document embeddings (from the 'chunks' variable) to the FAISS index.
# The 'add_documents' method returns a list of IDs corresponding to the documents added.
ids = vector_store.add_documents(documents=chunks)
#print("ids-> ",ids)

# Check how many documents were added and how many vectors are in the index now.
# len(ids) gives the number of documents added, and vector_store.index.ntotal gives the total number of vectors in the index after the addition.
len(ids), vector_store.index.ntotal

question = "how to gain muscle mass?"
result = vector_store.search(query=question, k=5, search_type='similarity')
#print("result-> ", result)
vector_store.save_local(db_name)

