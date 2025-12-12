from config import *
import os
from google.genai import types

def get_file_content(working_directory, file_path):

    try:
        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.abspath(full_path)

        if(not full_path.startswith(os.path.abspath(working_directory))):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if(not os.path.isfile(full_path)):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        if(len(file_content_string) >= MAX_CHARS):
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'

    except Exception as e:
        return f'Error: {e}'
    
    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to read, relative to the working directory.",
            ),
        },
    ),
)