import os
import re
import uuid
import tempfile
from utils.lida_utils import CustomTextGenerator, TextGenerationResponse
from config import GOOGLE_MODELS, GROQ_MODELS, OPENAI_MODELS, GROQ_API_KEY, AZURE_API_KEY, GOOGLE_API_KEY
import streamlit as st
import base64
from utils.message_utils import get_file_messages
import requests
import time


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
    """
    Extracts the code block inside triple backticks and removes any line that contains only the word 'python'.
    If no code block is found, returns the original text.
    """
    # Use regex to find text inside triple backticks
    match = re.search(r'```(.*?)```', text, re.DOTALL)
    if match:
        code_block = match.group(1)
        # Remove lines that contain only the word 'python'
        filtered_code = "\n".join(line for line in code_block.splitlines() if line.strip().lower() != "python")
        return filtered_code
    return text  # Return text if no match is found

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
            
            return_dict = {
                "full_filename": new_file_path,
                "pretty_name": title
            }
            return return_dict
        
        return None
    except Exception as e:
        print(f"An error occurred in get_new_filename: {e}")
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

def replace_triple_quotes(code_snippet):
    """
    Replaces all instances of triple quotes (\"\"\") in a given code snippet with escaped triple quotes (\\"\\").

    Parameters:
        code_snippet (str): The code snippet as a string.

    Returns:
        str: The modified code snippet with triple quotes replaced.
    """
    return code_snippet.replace('"""', r'\"\"\"')

def clean_set_page_config(code):
    """
    Ensures only one `st.set_page_config` line exists in the provided code, 
    and keeps the one with the 🤖 emoji.

    Args:
        code (str): The input Python code as a string.

    Returns:
        str: The cleaned Python code with only one `st.set_page_config` line.
    """
    lines = code.splitlines()
    set_page_config_lines = [
        line for line in lines if "st.set_page_config" in line
    ]

    # Find the line with the 🤖 emoji, default to the first one if not found
    selected_line = next(
        (line for line in set_page_config_lines if "🤖" in line), 
        set_page_config_lines[0] if set_page_config_lines else None
    )

    # Remove all `st.set_page_config` lines from the original lines
    cleaned_lines = [
        line for line in lines if "st.set_page_config" not in line
    ]

    # Add the selected `st.set_page_config` line back, if found
    if selected_line:
        cleaned_lines.insert(1, selected_line)

    return "\n".join(cleaned_lines)

def add_to_file(new_content, file_path):

    # Read the content of the current file
    with open(file_path, 'r') as f:
        content = f.read()

    # Modify the content
    new_content = f"{content}\n\n{new_content}"

    # Write to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write(new_content)
        temp_file_name = temp_file.name

    # Replace the original file with the temporary file
    os.replace(temp_file_name, file_path)

import json
import ast

def fix_json(json_str):
    """
    Fixes a JSON string that uses single quotes instead of double quotes.

    Args:
        json_str (str): The JSON string to validate and fix.

    Returns:
        str: A corrected JSON string with double quotes.
    """
    try:
        # Try to load the string as valid JSON
        json_obj = json.loads(json_str)
        return str(json.dumps(json_obj, indent=4))  # Return pretty-printed JSON
    except json.JSONDecodeError as e:
        try:
            print(e)
            # Attempt to parse using ast.literal_eval
            json_obj = ast.literal_eval(json_str)
            return str(json.dumps(json_obj, indent=4))
        except (ValueError, SyntaxError):
            raise ValueError("Invalid JSON format. Unable to fix.")

def choose_text_generator(model: str):
    if model in GROQ_MODELS:
        groq_generator = CustomTextGenerator(
            model=model,
            api_type="groq",
            api_key=GROQ_API_KEY,
            )
        return groq_generator
    elif model in GOOGLE_MODELS:
        google_generator = CustomTextGenerator(
            model=model,
            api_type="google",
            api_key=GOOGLE_API_KEY,
            )
        return google_generator
    elif model in OPENAI_MODELS:
        azure_generator = CustomTextGenerator(
            model=model,
            api_type="azure",
            api_key=AZURE_API_KEY,
            )
        return azure_generator
    else:
        raise ValueError(f"Unknown model name: {model}")
    
def parse_model_response(response: TextGenerationResponse):
    return clean_set_page_config(extract_message(response.text[0]['content']))

def get_base64_of_bin_file(png_file: str) -> str:
    with open(png_file, "rb") as f:
        return base64.b64encode(f.read()).decode()


@st.cache_resource
def build_markup_for_logo(png_file: str) -> str:
    binary_string = get_base64_of_bin_file(png_file)
    return f"""
            <style>
                [data-testid="stSidebarHeader"] {{
                    background-image: url("data:image/png;base64,{binary_string}");
                    background-repeat: no-repeat;
                    background-size: 200px;
                    padding-bottom: 5rem;
                    background-position: top center;
                }}
            </style>
            """


def get_last_dashboard(file_name):
    messages = get_file_messages(file_name)
    last_messages = messages[-2:]
    return last_messages

# Function to execute newly generated code and update the display
def execute_new_code(new_code, placeholder):
    # Create a local dictionary to execute user code safely
    local_context = {}
    exec(new_code, {}, local_context)

# Function to call the error correction service
def correct_code_remotely(code_snippet, extra_context, file_name):
    url = "http://127.0.0.1:8000/correct_code/"  # Replace with the service URL
    payload = {
        "code": code_snippet,
        "extra_context": extra_context,
        "file_name": file_name,
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("corrected_code", code_snippet)
        else:
            st.error(f"Error during code correction: {response.text}")
            return code_snippet
    except Exception as e:
        st.error("The code corrector microservice is not up and running right now. Please try again later.")
        print(e)
 
def wait_for_file(file_path, check_interval=1):
    """
    Waits for a file to be created at the specified path. 
    Checks for the file's existence every `check_interval` seconds.
    
    Parameters:
    - file_path (str): The path of the file to check for.
    - check_interval (int): Time in seconds between existence checks.
    
    Returns:
    - bool: True if the file is found, False if interrupted.
    """
    tries = 6
    trie = 0
    try:
        while not os.path.exists(file_path):
            time.sleep(check_interval)
            if trie > tries:
                return False
            trie += 1
        return True
    except KeyboardInterrupt:
        return False

def generate_pages():
    # List all files ending with .py in the directory
    folder_name = "Your_Dashboards"
    python_files = [f for f in os.listdir(folder_name) if f.endswith('.py')]

    # Sort the files alphabetically
    python_files.sort()

    dashboard_pages = []
    for file in python_files:
        cleaned = file.replace('_', ' ').replace('.py', '')
        dashboard_pages.append(st.Page(
            f"{folder_name}/{file}",
            title=cleaned,
            icon=":material/smart_toy:",
            )
        )
    return dashboard_pages