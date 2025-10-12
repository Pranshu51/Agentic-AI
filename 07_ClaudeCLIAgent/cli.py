from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import requests
from pydantic import BaseModel,Field
from typing import Optional

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the OpenAI client for Gemini API
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def run_command(cmd: str):
    result = os.system(cmd)
    return result


def get_weather(city:str):
  url=f"https://wttr.in/{city.lower()}?format=%c+%t"
  response = requests.get(url)

  if response.status_code == 200:
    return f"The current weather in {city} is {response.text}"
  
  return "Sorry, I couldn't fetch the weather information right now."

available_tools ={
    "get_weather": get_weather,
    "run_command": run_command
}


# ===================== SYSTEM PROMPT =====================
SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN, and OUTPUT steps.

You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.
You can also call a tool if required from the available list of tools.
for every tool call wait for the observe step which is the output from the called tool.

Rules:
- Strictly follow the given JSON output format.
- Only run one step at a time.
- The sequence of steps is START (where user gives input), PLAN (which can repeat multiple times), and finally OUTPUT (which goes to the user).
- Always return exactly ONE valid JSON object.
- Do NOT include extra explanations, markdown, or multiple JSON objects.

Output JSON Format:
{
  "step": "START" | "PLAN" | "OUTPUT" | "TOOL",
  "content": "string", "tool": "string", "input": "string", "output": "string"
}

Available Tools:
- get_weather(city: str): takes city name as input string and returns the current weather information for that city.
- run_command(cmd: str): takes a system linux command as input string and executes  the command on the user's system, return the output from that command.


Example 1:

START: Hey, can you solve 2 + 3 * 5 / 10
PLAN: { "step": "PLAN", "content": "Seems like user is interested in math problem" }
PLAN: { "step": "PLAN", "content": "We should use BODMAS method" }
PLAN: { "step": "PLAN", "content": "Multiplying 3 * 5 = 15" }
PLAN: { "step": "PLAN", "content": "Now 2 + 15 / 10" }
PLAN: { "step": "PLAN", "content": "15 / 10 = 1.5" }
PLAN: { "step": "PLAN", "content": "2 + 1.5 = 3.5" }
OUTPUT: { "step": "OUTPUT", "content": "3.5" }

Example 2:

START:What is the weather of delhi?
PLAN: { "step": "PLAN", "content": "Seems like user is interested in getting weather information" }
PLAN: { "step": "PLAN", "content": "lets see if we have any available tool from the list of available tool" }
PLAN: { "step": "PLAN", "content": "Great , we have get_weather tool available for the query" }
PLAN: { "step": "PLAN", "content": "I need to call weather tool for delhi as input city" }
PLAN: { "step": "TOOL", "tool": "get_weather", "input": "delhi" }
PLAN: { "step": "OBSERVE", "tool": "get_weather", "output": "The current weather in delhi is ☀️ 30°C" }
PLAN: { "step": "PLAN", "content": "Great i got the weather info about delhi" }
OUTPUT: { "step": "OUTPUT", "content": "The current weather in delhi is  sunny with ☀️ 30°C" }

"""
# =========================================================

print("\n\n\n\n")

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None, description="The optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call.")
    input: Optional[str] = Field(None, description="The input params for the tool")

# Initialize message history
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

while True:
# Take user query
  user_query = input("👉 Enter your query: ")
  message_history.append({"role": "user", "content": user_query})

  while True:
      # Send the conversation to Gemini model
      response = client.chat.completions.parse(
          model="gemini-2.5-flash",
          response_format=MyOutputFormat,
          messages=message_history
      )

      # Get raw model output
      raw_result = response.choices[0].message.parsed

      # Debug: Print what model actually returned (optional)
      # print("RAW RESPONSE:", raw_result)

      try:
          # Parse the JSON result
          parsed_result = response.choices[0].message.parsed
          # If parsed_result is a string, parse again
          if isinstance(parsed_result, str):
              parsed_result = json.loads(parsed_result)
          # If parsed_result is a list, use the first element
          if isinstance(parsed_result, list):
              parsed_result = parsed_result[0]
      except json.JSONDecodeError:
          print("⚠️ The model returned invalid JSON. Skipping this step.")
          print("Response was:", raw_result)
          # Fallback: print the plain string if it's not JSON
          if raw_result.startswith('"') and raw_result.endswith('"'):
              # Decode unicode escapes for better readability
              print("🤖 Model output:", bytes(raw_result.strip('"'), "utf-8").decode("unicode_escape"))
          break

      # Append assistant message to history
      # Convert to JSON string if it's a Pydantic object or dict
      if isinstance(raw_result, (dict, BaseModel)):
          message_history.append({"role": "assistant", "content": json.dumps(raw_result if isinstance(raw_result, dict) else raw_result.model_dump())})
      else:
          message_history.append({"role": "assistant", "content": str(raw_result)})

      # Handle different reasoning stages
      if parsed_result.step == "START":
          print("💡 The model has started the reasoning process:", parsed_result.content)
          continue

      if parsed_result.step == "TOOL":
          tool_to_call = parsed_result.tool
          tool_input = parsed_result.input
          print(f"🔧 {tool_to_call} ({tool_input})")

          tool_response = available_tools[tool_to_call](tool_input)
          print(f"🔧 {tool_to_call} ({tool_input}) = {tool_response}")
          message_history.append({"role": "developer", "content": json.dumps({
              "step": "OBSERVE",
              "tool": tool_to_call,
              "input": tool_input,
              "output": tool_response
          })})
          continue

      if parsed_result.step == "PLAN":
          print("🧠 The model is planning:", parsed_result.content)
          continue

      if parsed_result.step == "OUTPUT":
          print("🤖 The model has completed the reasoning process:", parsed_result.content)
          break


print("\n\n\n\n")




