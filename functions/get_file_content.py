#from get_files_info.py import get_files_info
import os
from config.py import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    """
    if file content outside of file path
    f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'


        with open(file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        # After reading the first MAX_CHARS...
        if f.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"
