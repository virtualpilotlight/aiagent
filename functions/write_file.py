def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'


        with open(file_path, "w") as f:
            f.write(content)

        return file_content_string
    except Exception as e:
        return f"Error: {e}"
