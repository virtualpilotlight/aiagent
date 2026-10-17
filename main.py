import os
from dotenv import load_dotenv

from openai import OpenAI

import argparse

from prompts import system_prompt

from functions.call_function import available_functions, call_function

import json

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

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
if message.tool_calls:
    for tool_call in message.tool_calls:
        result_message = call_function(tool_call, verbose=args.verbose)
        if not result_message["content"]:
            raise Exception(f"Function {tool_call.function.name} returned empty content")
        if args.verbose:
            print(f"-> {result_message['content']}")

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
