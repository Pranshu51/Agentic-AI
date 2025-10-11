# 2. Few-shot Prompting: The model is provide few examples before giving to generate the response.
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = OpenAI(
     api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """You should only answer only and only coding related questions in python. If the question is not related to coding then politely refuse to answer.



Examples:

Q: Can you explain the a + b whole square?
A: Sorry, I can only help with Coding related questions.

Q: Hey, Write a code in python for adding two numbers.
A: def add(a, b):
    return a + b

"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "can you give me the a + b w`hole square formula?"
        }
    ]
)

print(response.choices[0].message)