from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

from google.genai import types

fxDict ={
    'get_file_content': get_file_content,
    'get_files_info': get_files_info,
    'run_python_file': run_python_file,
    'write_file': write_file,
}

def call_function(function_call_part, verbose=False):
    
    fxName = function_call_part.name

    if verbose:
        print(f"Calling function: {fxName}({function_call_part.args})")
    else: 
        print(f" - Calling function: {fxName}")

    if fxName not in fxDict:
       return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fxName,
                    response={"error": f"Unknown function: {fxName}"},
                )
            ],
        )
    
    result = fxDict[function_call_part.name]("./calculator", **function_call_part.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=fxName,
                response={"result": result},
            )
        ],
    )