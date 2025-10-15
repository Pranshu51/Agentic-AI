import os
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI  # OpenAI-compatible interface for Gemini
import json

# -------------------------------
# 1️⃣ Load API keys & credentials
# -------------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# -------------------------------
# 2️⃣ OpenAI-compatible Gemini client
# -------------------------------
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

# -------------------------------
# 3️⃣ Mem0 configuration (with Neo4j)
# -------------------------------
config = {
    "version": "v1.1",
    "embedder": {
        "provider": "huggingface",
        "config": {"model": "all-MiniLM-L6-v2"}
    },
    "llm": {
        "provider": "gemini",
        "config": {"model": "gemini-2.5-flash"}
    },
    "graph_store": {   # ✅ Added Neo4j config here
        "provider": "neo4j",
        "config": {
            "url": NEO4J_URI,
            "username": NEO4J_USERNAME,
            "password": NEO4J_PASSWORD
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

mem_client = Memory.from_config(config)

# -------------------------------
# 4️⃣ Chat loop + memory
# -------------------------------
while True:
    user_query = input("> ")

    # Search memory
    search_memory = mem_client.search(query=user_query, user_id="pranshu")
    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}"
        for mem in search_memory.get("results", [])
    ]
    print("Found Memories:", memories)

    SYSTEM_PROMPT = f"""
    Here is the context about the user:
    {json.dumps(memories, indent=2)}
    """

    # Generate response using Gemini
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    ai_response = response.choices[0].message.content
    print("AI:", ai_response)

    # Store conversation in Mem0
    mem_client.add(
        user_id="pranshu",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ]
    )

    print("✅ Memory has been saved...\n")




















# import os
# from dotenv import load_dotenv
# from mem0 import Memory
# from openai import OpenAI  # Using OpenAI-compatible interface for Gemini
# import json

# # -------------------------------
# # 1️⃣ Load Gemini API key
# # -------------------------------
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # -------------------------------
# # 2️⃣ OpenAI-compatible client for Gemini
# # -------------------------------
# client = OpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai"
# )

# # -------------------------------
# # 3️⃣ Mem0 configuration
# # -------------------------------
# config = {
#     "version": "v1.1",
#     "embedder": {
#         "provider": "huggingface",  # Free embedding
#         "config": {"model": "multi-qa-MiniLM-L6-cos-v1"}
#     },
#     "llm": {
#         "provider": "gemini",
#         "config": {"model": "gemini-2.5-flash"}  # ✅ Actual Gemini model
#     },
#     "vector_store": {
#         "provider": "qdrant",
#         "config": {
#             "host": "localhost",
#             "port": 6333
#         }
#     }
# }

# mem_client = Memory.from_config(config)

# # -------------------------------
# # 4️⃣ Chat loop + memory
# # -------------------------------
# while True:
#     user_query = input("> ")
#     search_memory = mem_client.search(query=user_query)
#     memories= [
#         f"ID: {mem.get("id")}\Memory : {mem.get("memory")}" for mem in search_memory
#     ]
    
#     print("Found Memories", memories)

#     SYSTEM_PROMPT = f"""
#     Here is the context about the user:
#     {json.dumps(memories)}
#     """
#     # Generate response using Gemini
#     response = client.chat.completions.create(
#         model="gemini-2.5-flash",
#         messages=[
#             {"role": "system" , "content": SYSTEM_PROMPT},
#             {"role": "user", "content": user_query}
#             ]
#     )
#     ai_response = response.choices[0].message.content
#     print("AI:", ai_response)

#     # Store conversation in Mem0
#     mem_client.add(
#         user_id="pranshu",
#         messages=[
#             {"role": "user", "content": user_query},
#             {"role": "assistant", "content": ai_response}
#         ]
#     )


# print("memory has been saved...")