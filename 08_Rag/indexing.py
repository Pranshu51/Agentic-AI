# #go to langchain document loader website for pypdf load
# #then go to langchain text splitter website for chunking and text splitting
# #search langchain openai embeddings for vector embeddings
# #search langchain qdrant db

# go to langchain document loader website for pypdf load
# then go to langchain text splitter website for chunking and text splitting
# search langchain google genai embeddings for vector embeddings
# search langchain qdrant db

# go to langchain document loader website for pypdf load
# then go to langchain text splitter website for chunking and text splitting
# search langchain google genai embeddings for vector embeddings
# search langchain qdrant db

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings  # ✅ Free embeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os

# Load environment variables (if any)
load_dotenv()

# Path to your PDF
pdf_path = Path(__file__).parent / "report.pdf"

# 1️⃣ Load PDF
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()  # List of Document objects (page by page)

# 2️⃣ Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)
chunks = text_splitter.split_documents(docs)

# 3️⃣ Initialize free HuggingFace embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4️⃣ Store embeddings in Qdrant
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

print("✅ Indexing of PDF into Qdrant is done successfully!")













































# from pathlib import Path
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter #for text splitting
# from langchain_openai import OpenAIEmbeddings #for vector embeddings
# from langchain_qdrant import QdrantVectorStore #for vector db
# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# client = OpenAI(
#      api_key=api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )


# pdf_path = Path(__file__).parent / "report.pdf"

# #load this file in python program
# loader = PyPDFLoader(file_path=pdf_path)
# docs = loader.load()#this docs will give page by page text

# #Split the docs into smaller chunks

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
# chunk_overlap=400
# )

# chunks = text_splitter.split_documents(docs)#this will give smaller chunks of text

# #Vector Embeddings

# embedding_model = OpenAIEmbeddings(
#   model="text-embedding-3-large"
# )

# vector_store = QdrantVectorStore.from_documents(
#   documents=chunks,
#   embedding_model=embedding_model,
#   url="http://localhost:6333",
#   collection_name="learning_rag",
# )

# print("Indexing of document is done..")