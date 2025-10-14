#search mongodb in the langgraph.github you will get methdo to move furtherafter up docker of mongodb

from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import os
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver


load_dotenv()

# ✅ Read key (DO NOT overwrite it)
google_api_key = os.getenv("GEMINI_API_KEY")

if not google_api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# ✅ Initialize model with key
llm = init_chat_model("google_genai:gemini-2.0-flash", api_key=google_api_key)

class State(TypedDict):
  messages:Annotated[list, add_messages]

def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}




graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)


graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

#(START) -> chatbot -> samplenode -> (END)

graph = graph_builder.compile()

def compile_graph_with_checkpointer(checkpointer) :
   return graph_builder.compile(checkpointer=checkpointer)
     
DB_URI = "mongodb://admin:admin@localhost:27017" #admin => pass and mongodb => db ,lg => db name
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer=checkpointer)

    config = {
            "configurable": {
                "thread_id": "pranshu" #user_id
            }
        }

    for chunk in graph_with_checkpointer.stream(
    State({"messages":["what is my name and what am i learning"]}),  #HI, My name is Pranshu <==prev state
    config,
    stream_mode="values"
    ):
       chunk["messages"][-1].pretty_print()

#(START) -> chatbot -> samplenode -> (END)
#state = {messages: ["hey there"]}
#node runs: chatbot(state: ["hey there"]) -> ["hi , this is the messgae from chatbot node"]

#checkpointer (pranshu) = HI, My name is Pranshu