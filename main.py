import os
from dotenv import load_dotenv

from openai import OpenAI

import argparse

from prompts import system_prompt

from functions.call_function import available_functions

import json

from functions.get_files_info import schema_get_files_info

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

#prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
)

message = response.choices[0].message
if message.tool_calls != None:
    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")

usage = response.usage
if usage is None:
    raise RuntimeError(
        "Response has no usage data, which likely means the API request failed."
    )

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {usage.prompt_tokens}")
    print(f"Response tokens: {usage.completion_tokens}")

print("Response:")
print(response.choices[0].message.content)
