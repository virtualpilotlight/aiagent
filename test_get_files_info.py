from functions.get_files_info import get_files_info


def indent(text: str, spaces: int) -> str:
    pad = " " * spaces
    return "\n".join(pad + line for line in text.splitlines())


def show(label: str, directory: str) -> None:
    result = get_files_info("calculator", directory)
    print(f"Result for {label}:")
    # Directory listings are indented 2 spaces; errors are indented 4
    print(indent(result, 4 if result.startswith("Error:") else 2))
    print()


if __name__ == "__main__":
    show("current directory", ".")
    show("'pkg' directory", "pkg")
    show("'/bin' directory", "/bin")
    show("'../' directory", "../")
