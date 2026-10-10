import os
import sys

# 1. Get the absolute path of the directory containing the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Move up one level to the parent directory
parent_dir = os.path.dirname(current_dir)

# 3. Add the parent directory to the sys.path
sys.path.append(parent_dir)

from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'


        with open(target_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string
    except Exception as e:
        return f"Error: {e}"
