import os
import sys
import argparse

from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from functions.call_function import available_functions, call_function

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

if args.verbose:
    print(f"User prompt: {args.user_prompt}")

for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    usage = response.usage
    if usage is None:
        raise RuntimeError(
            "Response has no usage data, which likely means the API request failed."
        )
    if args.verbose:
        print(f"Prompt tokens: {usage.prompt_tokens}")
        print(f"Response tokens: {usage.completion_tokens}")

    message = response.choices[0].message
    messages.append(message)  # assistant turn, including any tool_calls

    if not message.tool_calls:
        print("Final response:")
        print(message.content)
        break

    for tool_call in message.tool_calls:
        result_message = call_function(tool_call, verbose=args.verbose)
        if not result_message["content"]:
            raise Exception(
                f"Function {tool_call.function.name} returned empty content"
            )
        if args.verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)  # role: tool, tool_call_id, content
else:
    print("Error: reached the maximum of 20 iterations without a final response.")
    sys.exit(1)
