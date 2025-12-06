import os

def get_files_info(working_directory, directory="."):

    try:
        full_path = os.path.join(working_directory, directory)
        full_path = os.path.abspath(full_path)
        
        if(not full_path.startswith(os.path.abspath(working_directory))):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if(not os.path.isdir(full_path)):
            return f'Error: "{directory}" is not a directory'
        
        files = [os.path.join(full_path, f) for f in os.listdir(full_path)]
        lines = [f'- {os.path.basename(f)}: file_size={os.path.getsize(f)} bytes, is_dir={os.path.isdir(f)}' for f in files]
        lines = [f"Result for {"current" if directory == "." else "'" + directory + "'"} directory:"] + lines
    
    except Exception as e:
        return f'Error: {e}'
    
    return "\n".join(lines)