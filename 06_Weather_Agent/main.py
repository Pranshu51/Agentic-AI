#weather api ==> https://wttr.in/{city}?format=%c+%t
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = OpenAI(
     api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_weather(city:str):
  url=f"https://wttr.in/{city.lower()}?format=%c+%t"
  response = requests.get(url)

  if response.status_code == 200:
    return f"The current weather in {city} is {response.text}"
  
  return "Sorry, I couldn't fetch the weather information right now."


def main():
  user_query = input("> ")
  response = client.chat.completions.create(
      model="gemini-2.5-flash",
      messages=[
          {
              "role": "user",
              "content": user_query
          }
      ]
  )

  print(f"🤖: {response.choices[0].message.content}")

main()  

