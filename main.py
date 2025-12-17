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
from functions.call_function import call_function

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

    for i in range(0,20):

        try: 
            response = client.models.generate_content(
                model = 'gemini-2.5-flash', 
                contents = messages,
                config= config,
            )

            if not response.usage_metadata:
                raise RuntimeError("Gemini API response appears to be malformed")
            
            for candidate in response.candidates: # type: ignore
                messages.append(candidate.content) # type: ignore
            
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            fxCalls = response.function_calls

            if(fxCalls is not None):

                results = []

                for fx in fxCalls:
                    # print(f"Calling function: {fx.name}({fx.args})")
                    fxResult = call_function(fx, "--verbose" in sys.argv)

                    if (fxResult.parts is None or 
                        fxResult.parts[0].function_response is None or 
                        fxResult.parts[0].function_response.response is None
                    ):
                        raise RuntimeError("Error getting function result")
                    
                    if "--verbose" in sys.argv:
                        print(f"-> {fxResult.parts[0].function_response.response}")
                    
                    results += fxResult.parts[0].function_response.response["result"]

                    fxContent = types.Content(
                        role="user", 
                        parts=[types.Part(text = "\n".join(results))]
                    )

                    messages.append(fxContent)

            else:
                if response.text is not None:
                    print("Final Response:")
                    print(response.text)
                    break

            if("--verbose" in sys.argv):
                print(f"User prompt: {args.prompt}")
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {response_tokens}")

        except Exception as e:
            print(f"Error: executing agent: {e}")
            continue
        



if __name__ == "__main__":
    main()
