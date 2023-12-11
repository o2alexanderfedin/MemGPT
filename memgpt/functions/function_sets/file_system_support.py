from typing import Optional, List
import os
import json
import requests


from ...constants import MESSAGE_CHATGPT_FUNCTION_MODEL, MESSAGE_CHATGPT_FUNCTION_SYSTEM_MESSAGE, MAX_PAUSE_HEARTBEATS
from ...openai_tools import completions_with_backoff as create


def list_directory_contents(self, path: str, recursive: bool = False) -> List[str]:
    """
    List the contents of a directory.

    Args:
        path (str): The directory path to list.
        recursive (bool): If True, list contents recursively. Defaults to False.

    Returns:
        List[str]: List of file and directory paths.
    """
    contents = []
    if recursive:
        for root, dirs, files in os.walk(path):
            for name in dirs:
                contents.append(os.path.join(root, name))
            for name in files:
                contents.append(os.path.join(root, name))
    else:
        with os.scandir(path) as entries:
            for entry in entries:
                contents.append(entry.path)
    return contents


def create_directory(self, path: str):
    """
    Create a new directory.

    Args:
        path (str): The directory path to create.
    """
    os.makedirs(path, exist_ok=True)


def delete_directory(self, path: str):
    """
    Delete a directory.

    Args:
        path (str): The directory path to delete.
    """
    os.rmdir(path)


def create_file(self, path: str, content: str = ''):
    """
    Create a new file with optional content.

    Args:
        path (str): The file path to create.
        content (str): Initial content of the file. Defaults to empty string.
    """
    with open(path, 'w') as file:
        file.write(content)


def delete_file(self, path: str):
    """
    Delete a file.

    Args:
        path (str): The file path to delete.
    """
    os.remove(path)


def is_directory(self, path: str) -> bool:
    """
    Check if a path is a directory.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a directory, False otherwise.
    """
    return os.path.isdir(path)


def is_file(self, path: str) -> bool:
    """
    Check if a path is a file.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a file, False otherwise.
    """
    return os.path.isfile(path)


def does_path_exist(self, path: str) -> bool:
    """
    Check if a path exists.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    return os.path.exists(path)


def get_file_size(path: str) -> Optional[int]:
    """
    Get the size of a file in bytes.

    Args:
        path (str): The file path to get the size of.

    Returns:
        Optional[int]: The size of the file in bytes, or None if the file does not exist or is a directory.
    """
    try:
        if os.path.isfile(path):
            return os.path.getsize(path)
        else:
            return None
    except OSError as e:
        print(f"Error: {e}")
        return None
