#from get_files_info.py import get_files_info
import os

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

        lines = []
        for name in os.listdir(target_dir):
            item_path = os.path.join(target_dir, name)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            lines.append(f"- {name}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"
