import os

def create_folder_by_file_path(file_path: str) -> None:
    """
    Creates a folder at the specified path.
    :param folder_path: Path to the folder to create.
    """
    try:
        folder_path = os.path.dirname(file_path)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder created at {folder_path}")
    except Exception as e:
        print(f"Error creating folder: {e}")
    
def save_content_to_file(file_path: str, content: str) -> None:
    """
    Saves the provided content to a file.
    :param file_path: Path to the file where content will be saved.
    :param content: The content to write to the file.
    """
    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Content saved to {file_path}")
    except Exception as e:
        print(f"Error saving content to file: {e}")

def read_file_content(file_path: str) -> str:
    """
    Reads and returns the content of a specified file.
    :param file_path: Path to the file to read.
    :return: Content of the file as a string.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""
def read_file_binary_content(file_path: str) -> str:
    """
    Reads and returns the content of a specified file.
    :param file_path: Path to the file to read.
    :return: Content of the file as a string.
    """
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def list_files_in_folder(folder_path: str, include_subfolders: bool = False) -> list:
    """
    Lists all files in the given folder and optionally in subfolders.
    :param folder_path: Path to the folder to list files from.
    :param include_subfolders: Whether to include files in subfolders.
    :return: A list of file paths in the folder and subfolders.
    """
    file_list = []
    try:
        for root, _, files in os.walk(folder_path) if include_subfolders else [(folder_path, [], os.listdir(folder_path))]:
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    file_list.append(file_path)
        return file_list
    except Exception as e:
        print(f"Error listing files in folder: {e}")
        return []

def read_files_by_extension(folder_path: str, extension: str, include_subfolders: bool = False) -> dict:
    """
    Reads all files with the specified extension in a folder and optionally in subfolders, returning their contents.
    :param folder_path: Path to the folder to search.
    :param extension: File extension to filter by (e.g., ".txt").
    :param include_subfolders: Whether to include files in subfolders.
    :return: Dictionary with file names as keys and their contents as values.
    """
    files_content = {}
    try:
        for root, _, files in os.walk(folder_path) if include_subfolders else [(folder_path, [], os.listdir(folder_path))]:
            for file in files:
                if file.endswith(extension):
                    file_path = os.path.join(root, file)
                    files_content[file_path] = read_file_content(file_path)
        return files_content
    except Exception as e:
        print(f"Error reading files by extension: {e}")
        return {}

def read_all_files_in_folder(folder_path: str, include_subfolders: bool = False) -> dict:
    """
    Reads all files in a folder and optionally in subfolders, returning their contents.
    :param folder_path: Path to the folder to read files from.
    :param include_subfolders: Whether to include files in subfolders.
    :return: Dictionary with file names as keys and their contents as values.
    """
    files_content = {}
    try:
        for root, _, files in os.walk(folder_path) if include_subfolders else [(folder_path, [], os.listdir(folder_path))]:
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    files_content[file_path] = read_file_content(file_path)
        return files_content
    except Exception as e:
        print(f"Error reading all files in folder: {e}")
        return {}
