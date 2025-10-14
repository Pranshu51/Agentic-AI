from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import os
from langchain.chat_models import init_chat_model


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

def samplenode(state: State):
    print("\n\ninside the samplenode node" , state)
    return {"messages": ["Sample message appended"]}


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

#(START) -> chatbot -> samplenode -> (END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages":["HI, My name is Pranshu"]}))
print("\n\nupdated_state", updated_state)