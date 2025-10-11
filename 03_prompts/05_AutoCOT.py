# # auto chai of thought prompting
# from openai import OpenAI
# import os
# import json
# from dotenv import load_dotenv
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# client = OpenAI(
#      api_key=api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# SYSTEM_PROMPT ="""
# You're an expert AI Assistant in resolving user queries using chain of thought
# You work on START, PLAN and OUPUT steps.
# You need to first PLAN what needs to be done. The PLAN can be multiple steps.
# Once you think enough PLAN has been done, finally you can give an OUTPUT.

# Rules:
# - Strictly Follow the given JSON output format
# - Only run one step at a time.
# - The sequence of steps is START (where user gives an input), PLAN (That can
#   be multiple times) and finally OUTPUT (which is going to the displayed to
#   the user).

# Output JSON Format:
# { "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

# Example:
# START: Hey, Can you solve 2 + 3 * 5 / 10
# PLAN: { "step": "PLAN", "content": "Seems like user is interested in math problem" }
# PLAN: { "step": "PLAN", "content": "looking at the problem, we should solve this using BODMAS method" }
# PLAN: { "step": "PLAN", "content": "Yes, The BODMAS is correct thing to be done here" }
# PLAN: { "step": "PLAN", "content": "first we must multiply 3 * 5 which is 15" }
# PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 15 / 10" }
# PLAN: { "step": "PLAN", "content": "We must perform divide that is 15 / 10 = 1.5" }
# PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 1.5" }
# PLAN: { "step": "PLAN", "content": "Now finally lets perform the add 3.5" }
# PLAN: { "step": "PLAN", "content": "Great, we have solved and finally left with 3.5 as ans" }
# OUTPUT: { "step": "OUTPUT", "content": "3.5" }

# """

# print("\n\n\n\n")



# message_history = [
#   {"role": "system", "content": SYSTEM_PROMPT},

# ]

# user_query = input("👉Enter your query: ")
# message_history.append({"role": "user", "content": user_query})

# while True:
#   response = client.chat.completions.create(
#     model="gemini-2.5-flash",
#     response_format={"type": "json_object"},
#     messages=message_history
#   )

#   raw_result = response.choices[0].message.content
#   message_history.append({"role": "assistant", "content": raw_result})
#   parsed_result = json.loads(raw_result)

#   if parsed_result.get("step") == "START":
#     print("💡 The model has started the reasoning process.",parsed_result.get("content"))
#     continue
#   if parsed_result.get("step") == "PLAN":
#     print("🧠 The model is planning.",parsed_result.get("content"))
#     continue
#   if parsed_result.get("step") == "OUTPUT":
#     print("🤖 The model has completed the reasoning process.",parsed_result.get("content"))
#     break


# print("\n\n\n\n")



# 2 method
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the OpenAI client for Gemini API
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ===================== SYSTEM PROMPT =====================
SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN, and OUTPUT steps.

You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.

Rules:
- Strictly follow the given JSON output format.
- Only run one step at a time.
- The sequence of steps is START (where user gives input), PLAN (which can repeat multiple times), and finally OUTPUT (which goes to the user).
- Always return exactly ONE valid JSON object.
- Do NOT include extra explanations, markdown, or multiple JSON objects.

Output JSON Format:
{
  "step": "START" | "PLAN" | "OUTPUT",
  "content": "string"
}

Example:

START: Hey, can you solve 2 + 3 * 5 / 10
PLAN: { "step": "PLAN", "content": "Seems like user is interested in math problem" }
PLAN: { "step": "PLAN", "content": "We should use BODMAS method" }
PLAN: { "step": "PLAN", "content": "Multiplying 3 * 5 = 15" }
PLAN: { "step": "PLAN", "content": "Now 2 + 15 / 10" }
PLAN: { "step": "PLAN", "content": "15 / 10 = 1.5" }
PLAN: { "step": "PLAN", "content": "2 + 1.5 = 3.5" }
OUTPUT: { "step": "OUTPUT", "content": "3.5" }
"""
# =========================================================

print("\n\n\n\n")

# Initialize message history
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

# Take user query
user_query = input("👉 Enter your query: ")
message_history.append({"role": "user", "content": user_query})

while True:
    # Send the conversation to Gemini model
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages=message_history
    )

    # Get raw model output
    raw_result = response.choices[0].message.content.strip()

    # Debug: Print what model actually returned (optional)
    # print("RAW RESPONSE:", raw_result)

    try:
        # Parse the JSON result
        parsed_result = json.loads(raw_result)
    except json.JSONDecodeError:
        print("⚠️ The model returned invalid JSON. Skipping this step.")
        print("Response was:", raw_result)
        break

    # Append assistant message to history
    message_history.append({"role": "assistant", "content": raw_result})

    # Handle different reasoning stages
    if parsed_result.get("step") == "START":
        print("💡 The model has started the reasoning process:", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠 The model is planning:", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("🤖 The model has completed the reasoning process:", parsed_result.get("content"))
        break

print("\n\n\n\n")




