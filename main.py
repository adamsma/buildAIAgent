import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import *

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")


    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ],
    )
    
    messages = [
        types.Content(role="user", parts=[types.Part(text = args.prompt)]),
    ]

    client = genai.Client(api_key=api_key)
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    response = client.models.generate_content(
        model = 'gemini-2.5-flash', 
        contents = messages,
        config= config,
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    fxCalls = response.function_calls

    if(fxCalls is not None):
        for fx in fxCalls:
            print(f"Calling function: {fx.name}({fx.args})")
    else:
        print(response.text)

    if("--verbose" in sys.argv):
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
