import sys
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


def read_text_file(self, path: str):
    """
    Reads from an existing text file with optional content.

    Args:
        path (str): The file path to read from.
    """
    with open(path, 'r') as file:
        return file.read(sys.maxsize)


def write_text_file(self, path: str, content: str = ''):
    """
    Writes a new or existing text file with optional content.

    Args:
        path (str): The file path to write to.
        content (str): Content to be written to the file. Defaults to empty string.
    """
    with open(path, 'w') as file:
        file.write(content)


def read_text_file_chunk(path: str, offset: int, chunk_size: int) -> Optional[str]:
    """
    Read a chunk of UTF-8 text from a file opened in shared mode, allowing other readers to access the file concurrently.
    The file is read assuming UTF-8 encoding. This function uses buffered reading to efficiently navigate to the
    correct character offset, avoiding issues with multi-byte characters.

    Args:
        path (str): The file path to read from.
        offset (int): The character offset from the beginning of the file.
        chunk_size (int): The number of characters to read.

    Returns:
        Optional[str]: The chunk of UTF-8 text read from the file, or None if the file does not exist, is not readable,
        or if an encoding error occurs.
    """
    try:
        with open(path, 'r', encoding='utf-8', errors='strict', buffering=8192) as file:
            # Read characters one by one up to the offset
            for _ in range(offset):
                if file.read(1) == '':
                    break  # End of file reached before the specified offset

            return file.read(chunk_size)
    except OSError as e:
        print(f"Error accessing the file: {e}")
        return None
    except UnicodeDecodeError as e:
        print(f"Encoding error in the file: {e}")
        return None


def write_text_file_chunk(path: str, data: str, char_offset: int) -> bool:
    """
    Write a chunk of UTF-8 text to a file at a specified character offset safely.
    This function handles UTF-8 encoding properly by reading up to the offset before writing.

    Args:
        path (str): The file path to write to.
        data (str): The UTF-8 text to write.
        char_offset (int): The character offset from the beginning of the file.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    try:
        # Read the existing content up to the offset
        with open(path, 'r', encoding='utf-8', buffering=8192) as file:
            existing_content = file.read(char_offset)

        # Combine the old content with the new data
        new_content = existing_content + data

        # Rewrite the file with the new content
        with open(path, 'w', encoding='utf-8', buffering=8192) as file:
            file.write(new_content)
            return True
    except OSError as e:
        print(f"Error accessing the file: {e}")
        return False
    except UnicodeDecodeError as e:
        print(f"Encoding error in the file: {e}")
        return False


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


def set_file_length(path: str, length: int) -> bool:
    """
    Set the length of a text file in characters. If the file is shorter than the specified length, it will be padded with spaces.
    If it's longer, it will be truncated.

    Args:
        path (str): The file path.
        length (int): The desired length of the file in characters.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    try:
        with open(path, 'r+', encoding='utf-8') as file:
            file_content = file.read()
            file_length = len(file_content)

            if file_length < length:
                # Pad the file with spaces if it's shorter than the desired length
                file.write(' ' * (length - file_length))
            elif file_length > length:
                # Truncate the file if it's longer than the desired length
                file.seek(0)
                file.write(file_content[:length])
                file.truncate()

        return True
    except OSError as e:
        print(f"Error accessing the file: {e}")
        return False
