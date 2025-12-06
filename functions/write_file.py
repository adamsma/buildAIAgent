import os
from config import *

def write_file(working_directory, file_path, content):

    try:

        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.abspath(full_path)

        if(not full_path.startswith(os.path.abspath(working_directory))):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        dir = os.path.dirname(full_path)
        if(not os.path.isdir(dir)):
            os.makedirs(dir)

        with open(full_path, "w") as f:
            f.write(content)


    except Exception as e:
         return f'Error: {e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'