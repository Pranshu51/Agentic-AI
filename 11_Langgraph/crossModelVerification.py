from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
import os
from groq import Groq

# ✅ Load environment variables
load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)

# ✅ Define state structure
class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

# ✅ Node 1: Main chatbot using LLaMA
def chatbot(state: State):
    print("\n🧠 Chatbot Node Running...")
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": state["user_query"]}],
        model="llama-3.3-70b-versatile",
    )
    state["llm_output"] = response.choices[0].message.content
    print("💬 LLaMA Response:", state["llm_output"])
    return state

# ✅ Node 2: Evaluation Node
def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    print("\n🔍 Evaluating response quality...")

    eval_prompt = f"""
    You are an expert evaluator. Judge if the following response is good, accurate, and relevant to the user query.
    Reply ONLY with 'yes' or 'no'.

    USER QUERY:
    {state['user_query']}

    MODEL RESPONSE:
    {state['llm_output']}
    """

    eval_response = client.chat.completions.create(
        messages=[{"role": "user", "content": eval_prompt}],
        model="llama-3.1-8b-instant",  # fast evaluation model
    )

    decision = eval_response.choices[0].message.content.strip().lower()
    print("🤖 Evaluation Model Output:", decision)

    if "yes" in decision:
        state["is_good"] = True
        return "endnode"
    else:
        state["is_good"] = False
        return "chatbot_gemini"

# ✅ Node 3: Gemini fallback chatbot
def chatbot_gemini(state: State):
    print("\n⚙️ Gemini Node Running...")
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": state["user_query"]}],
        model="openai/gpt-oss-120b",
    )
    state["llm_output"] = response.choices[0].message.content
    print("💬 Gemini Response:", state["llm_output"])
    return state

# ✅ Node 4: End node
def endnode(state: State):
    print("\n🏁 End Node Reached.")
    print("✅ Final Answer:", state["llm_output"])
    print("✨ Was response good?:", state.get("is_good"))
    return state

# ✅ Build LangGraph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    evaluate_response,
    {"chatbot_gemini": "chatbot_gemini", "endnode": "endnode"}
)
graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)
graph = graph_builder.compile()

# ✅ Take input dynamically
user_input = input("\n💬 Enter your question: ")
updated_state = graph.invoke({"user_query": user_input})

print("\n✅ Final State:", updated_state)
