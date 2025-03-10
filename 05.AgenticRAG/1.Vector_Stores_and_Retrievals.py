from imports import*

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
warnings.filterwarnings("ignore")

load_dotenv()


loader = PyMuPDFLoader(r"rag-dataset\gym supplements\1. Analysis of Actual Fitness Supplement.pdf")
loader.load()


# -------------------------------- GENERATE DOCUMENTS ----------------------------------------------------------
pdfs = []  # Initialize an empty list to store PDF file paths
for root, dirs, files in os.walk("rag-dataset"):  
    # os.walk() iterates through all directories and files inside "rag-dataset"
    # root -> The current folder being scanned  
    # dirs -> List of subdirectories in the current folder  
    # files -> List of files in the current folder  

    # Loop through all files in the current directory  
    for file in files:  
        if file.endswith(".pdf"):  # Check if the file has a ".pdf" extension  
            pdfs.append(os.path.join(root, file))  # Store the full file path  
print("pdf: ", pdfs)  # Print the list of PDF file paths  


docs = []  # Initialize an empty list to store the extracted document data

for pdf in pdfs:  # Loop through each PDF file path stored in the pdfs list
    loader = PyMuPDFLoader(pdf)  # Create a PDF loader using PyMuPDFLoader
    temp = loader.load()  # Load the content of the PDF (extract text and metadata)
    docs.extend(temp)  # Add the extracted content to the docs list

print("len docs-> ",len(docs))


#------------------------------------ DOCUMENT CHUNKING -------------------------------------------------------
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(docs)