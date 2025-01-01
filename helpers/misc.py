import os
import re
import uuid

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

def get_new_filename(file_contents):
    """
    Generates a new filename based on the st.title line in the given file contents.
    
    Args:
        file_contents (str): The string content of the file.
    
    Returns:
        str: The new filename, or None if no st.title(...) line is found.
    """
    try:
        # Look for the st.title("...") pattern
        match = re.search(r'st\.title\(["\'](.*?)["\']\)', file_contents)
        if match:
            # Extract the title and format it
            title = match.group(1)
            base_name = title.replace(" ", "_")
            new_file_name = base_name + ".py"
            new_file_path = os.path.join("Your_Dashboards", new_file_name)
            
            # Check if the file already exists
            if os.path.exists(new_file_path):
                # Append a random UUID before the .py extension
                unique_id = uuid.uuid4().hex[:8]  # Short UUID
                new_file_name = f"{base_name}_{unique_id}.py"
                new_file_path = os.path.join("Your_Dashboards", new_file_name)
            
            # print(f"New filename: {new_file_path}")
            return_dict = {
                "full_filename": new_file_path,
                "pretty_name": title
            }
            return return_dict
        
        print("No st.title(...) line found in the file.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
file_content = """
from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import json
import plotly.express as px

# Load the data
st.title("Combined Data Dashboard")
"""
# print(get_new_filename(file_content))