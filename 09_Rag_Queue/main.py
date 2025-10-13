import uvicorn
from server import app

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

openai_client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def main():
  uvicorn.run(app, port=8000, host="0.0.0.0")

main()  