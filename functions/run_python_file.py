import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args != None:
            command.extend(args)

        complete_process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

        return_str = ""
        if complete_process.returncode != 0:
            return_str = f"Process exited with code {complete_process.returncode}"

        if complete_process.stdout == "" and complete_process.stderr == "":
            return "No output produced"

        if complete_process.stdout != "":
            return_str += f"STDOUT:{complete_process.stdout}"

        if complete_process.stderr != "":
            return_str += f"STDERR:{complete_process.stderr}"

        #return f"Process exiteded with code {exit_code}\nSTDOUT: {complete_process.stdout}\nSTDERR: {complete_process.stderr}"
        return return_str

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "runs a python file within a specific directory",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "run a python file",
                },
            },
        },
    },
}
