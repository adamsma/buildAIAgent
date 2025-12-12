import os
import subprocess
from config import *
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):

    try:
        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.abspath(full_path)

        if(not full_path.startswith(os.path.abspath(working_directory))):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if(not os.path.isfile(full_path)):
            return f'Error: File "{file_path}" not found.'
        
        if(not file_path.endswith(".py")):
            return f'Error: "{file_path}" is not a Python file.'
        
        try:
            command = ["python3", full_path] + args
            proc = subprocess.run(args=command, timeout=30, capture_output=True, text = True)

            if((len(proc.stderr) + len(proc.stdout)) == 0):
                result = ["No output produced"]
            else:
                result = ["STDOUT: " + proc.stdout, "STDERR: " + proc.stderr]
            
            if(proc.returncode != 0):
                result += [f'Process exited with code {proc.returncode}']

        except Exception as e:
            return f"Error: executing Python file: {e}"

    except Exception as e:
        return f'Error: {e}'

    return "\n".join(result)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Eexecute the specified file with the provided arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to read, relative to the working directory.",
            ),"args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Arguments to be used when calling the specified function at the file path.",
            ),

        },
    ),
)