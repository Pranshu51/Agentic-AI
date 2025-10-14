from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
import os
from groq import Groq

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize Groq client safely
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found. Please set it in your .env file.")

client = Groq(api_key=api_key)

# ✅ Define state structure
class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

# ✅ Define chatbot node
def chatbot(state: State):
    print("chatbot node", state)
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": state.get("user_query")}],
        model="llama-3.3-70b-versatile",
    )
    state["llm_output"] = response.choices[0].message.content
    return state

# ✅ Decision node
def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    print("evaluate_response", state)
    # Placeholder condition (you can modify later)
    if False:
     return "endnode"
    return "chatbot_gemini"

# ✅ Second chatbot node
def chatbot_gemini(state: State):
    print("chatbot_gemini", state)
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": state.get("user_query")}],
        model="openai/gpt-oss-120b",
    )
    state["llm_output"] = response.choices[0].message.content
    return state

# ✅ End node
def endnode(state: State):
    print("endnode_Node", state)
    return state

# ✅ Build graph
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")

graph_builder.add_conditional_edges(
    "chatbot",
    evaluate_response,
    {
        "chatbot_gemini": "chatbot_gemini",
        "endnode": "endnode",
    }
)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

# ✅ Invoke graph
updated_state = graph.invoke({"user_query": "Hey what is 2+2?"})
print(updated_state)



















# from dotenv import load_dotenv
# from typing_extensions import TypedDict
# from typing import Optional,Literal
# from langgraph.graph import StateGraph, START, END
# import os

# from groq import Groq
# load_dotenv()

# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
# )

# class State(TypedDict):
#     user_query: str
#     llm_output: Optional[str]
#     is_good: Optional[bool]

# def chatbot(state: State):
#     response = client.chat.completions.create(
#     messages=[
#             {
#                 "role": "user",
#                 "content": state.get("user_query"),
#             }
#         ],
#         model="llama-3.3-70b-versatile",
#     )
#     state["llm_output"] = response.choices[0].message.content
#     return state


# def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
#     if True:
#         return "endnode"
    
#     return "chatbot_gemini"

# def chatbot_gemini(state: State):
#     response = client.chat.completions.create(
#     messages=[
#             {
#                 "role": "user",
#                 "content": state.get("user_query"),
#             }
#         ],
#         model="llama-3.3-70b-versatile",
#     )
#     state["llm_output"] = response.choices[0].message.content
#     return state



# def endnode(state: State):
#     return state

# graph_builder = StateGraph(State)

# graph_builder.add_node("chatbot", chatbot)
# graph_builder.add_node("chatbot_gemini", chatbot_gemini)
# graph_builder.add_node("endnode", endnode)


# graph_builder.add_edge(START,chatbot)
# graph_builder.add_conditional_edge("chatbot","evaluate_response")

# graph_builder.add_edge("chatbot_gemini","endnode")
# graph_builder.add_edge("endnode",END)

# graph = graph_builder.compile()

# updated_state  = graph.invoke(state({"user_query": "Hey what is 2+2?"}))
# print(updated_state)
