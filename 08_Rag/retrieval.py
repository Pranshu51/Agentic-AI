from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

openai_client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Initialize HuggingFace embedding model (free & local)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Connect to existing Qdrant collection
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

# Take user query
user_query = input("👉 Enter your query: ")

# Perform similarity search
search_results = vector_db.similarity_search(query=user_query)

# Build context from retrieved chunks
context = "\n\n\n".join([
    f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}"
    for result in search_results
])

SYSTEM_PROMPT = f"""
You are a helpful AI assistant who answers user queries based on the available
context retrieved from a PDF file along with page contents and page numbers.

You should only answer based on the following context.
Context:
{context}
"""

# Generate response using Gemini LLM
response = openai_client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
)

print(f"🤖: {response.choices[0].message.content}")
