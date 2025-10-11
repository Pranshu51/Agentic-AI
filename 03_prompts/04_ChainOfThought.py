# 2. Few-shot Prompting: The model is provide few examples before giving to generate the response.
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = OpenAI(
     api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT ="""
You're an expert AI Assistant in resolving user queries using chain of thought
You work on START, PLAN and OUPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.

Rules:
- Strictly Follow the given JSON output format
- Only run one step at a time.
- The sequence of steps is START (where user gives an input), PLAN (That can
  be multiple times) and finally OUTPUT (which is going to the displayed to
  the user).

Output JSON Format:
{ "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

Example:
START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN: { "step": "PLAN", "content": "Seems like user is interested in math problem" }
PLAN: { "step": "PLAN", "content": "looking at the problem, we should solve this using BODMAS method" }
PLAN: { "step": "PLAN", "content": "Yes, The BODMAS is correct thing to be done here" }
PLAN: { "step": "PLAN", "content": "first we must multiply 3 * 5 which is 15" }
PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 15 / 10" }
PLAN: { "step": "PLAN", "content": "We must perform divide that is 15 / 10 = 1.5" }
PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 1.5" }
PLAN: { "step": "PLAN", "content": "Now finally lets perform the add 3.5" }
PLAN: { "step": "PLAN", "content": "Great, we have solved and finally left with 3.5 as ans" }
OUTPUT: { "step": "OUTPUT", "content": "3.5" }

"""


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type": "json_object"},
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            # "content": "can you give me the a + b whole square formula?"
            "content": "can you give me the code for printing numbers from 1 to 100 in js?"
        },
        #manually keep appending by copying from the terminal
        {
          "role": "assistant",
          "content": json.dumps({ "step": "PLAN", "content": "The user wants JavaScript code to print numbers from 1 to 100." })
        },
         {
          "role": "assistant",
          "content": json.dumps({ "step": "PLAN", "content": "I need to provide JavaScript code. The code should use a loop to iterate from 1 to 100. Inside the loop, it should print the current number, typically using `console.log()`." })
        },
         {
          "role": "assistant",
          "content": json.dumps({ "step": "OUTPUT", "content": "```javascript\nfor (let i = 1; i <= 100; i++) {\n  console.log(i);\n}\n```" })
        },
          {
          "role": "assistant",
          "content": json.dumps({ "step": "OUTPUT", "content": "```javascript\nfor (let i = 1; i <= 100; i++) {\n  console.log(i);\n}\n```" })
        }
    ]
)

print(response.choices[0].message)