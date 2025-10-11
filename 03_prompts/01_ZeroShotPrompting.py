# 1. Zero-shot Prompting: The model is given a direct question or task without prior examples.
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = OpenAI(
     api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = "You should only answer only and only coding related questions in python. If the question is not related to coding then politely refuse to answer."

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "can you write the python code to print number from 1 to 1000"
        }
    ]
)

print(response.choices[0].message)