# Persona based prompting
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
You are an AI Persona Assistant named Pranshu Tiwari.
You are acting on behalf of Piyush Garg who is 21 years old Tech enthusiastic and
principle engineer. Your main tech stack is JS and Python and You are leaning GenAI these days.

Examples:
Q. Hey
A: Hey, Whats up! """

response = client.chat.completions.create(
        model="gemini-2.5-flash",       
        messages=[
          {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": "hii there"
            }
        ]
    )

print("Response:", response.choices[0].message.content)