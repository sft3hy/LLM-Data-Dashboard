import os
import re

def is_directory_empty(directory_path):
    """Check if the directory is empty."""
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"The directory {directory_path} does not exist.")
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"The path {directory_path} is not a directory.")
    return len(os.listdir(directory_path)) == 0

def generate_safe_filename(input_text, max_length=40):
    """
    Generates a safe filename by:
    - Removing non-alphanumeric characters.
    - Replacing spaces with underscores.
    - Capitalizing each word.
    - Truncating to the specified max length.

    Parameters:
        input_text (str): The input string to convert into a safe filename.
        max_length (int): The maximum length of the filename.

    Returns:
        str: A safe and formatted filename.
    """
    # Remove special characters
    safe_name = re.sub(r'[^\w\s]', '', input_text)
    # Replace spaces with underscores and capitalize each word
    safe_name = "_".join(word.capitalize() for word in safe_name.split())
    # Truncate to the maximum length
    return safe_name[:max_length]

def extract_message(text):
    # Use regex to find text inside triple backticks
    match = re.search(r'```(.*?)```', text, re.DOTALL)
    if match:
        return match.group(1)  # Return the text inside the backticks
    return text  # Return None if no match is found