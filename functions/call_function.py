import json

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file
]

def call_function(tool_call, verbose: bool = False) -> dict:
    # needs a loop
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    # if verbose
    print(f" - Calling function: {function_name}({function_args})")
    # else
    print(f" - Calling function: {function_name}")
