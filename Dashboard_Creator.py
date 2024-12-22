import streamlit as st
import os
import re
from helpers.gpt_4o_caller import generate_streamlit
from helpers.parse_file import extract_file_snippet
from helpers.dependency_ensurer import ensure_library_installed


# Page configuration
st.set_page_config(page_title="Dashboard Creator", page_icon="📊", layout="centered")

# Style for input bar (to mimic ChatGPT)
st.markdown(
    """
    <style>
    .input-box {
        width: 100%;
        border: none;
        outline: none;
        font-size: 16px;
        padding: 8px;
        background: transparent;
    }
    .input-box:focus {
        outline: none;
    }
    .submit-btn {
        padding: 8px 12px;
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
    }
    .submit-btn:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("Dashboard Creator")

# File Upload Section
st.subheader("Upload Files")

uploaded_files = st.file_uploader(
    "Drag and drop or select your file(s):",
    type=["kml", "geojson", "json", "csv", "zip"],  # Shapefiles are usually uploaded as zipped archives
    accept_multiple_files=True,
)
save_dir = "user_uploaded_files"

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_details = {
            "filename": uploaded_file.name,
            "filetype": uploaded_file.type,
        }
        # st.write("Uploaded file details:", file_details)
        
        # Save uploaded files (optional)
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, uploaded_file)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

def is_directory_empty(directory_path):
    """Check if the directory is empty."""
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"The directory {directory_path} does not exist.")
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"The path {directory_path} is not a directory.")
    return len(os.listdir(directory_path)) == 0

file_paths = []
all_file_snippets = {}

if not is_directory_empty(save_dir):
    st.subheader("Uploaded Files:")
    
    # List all files in the directory
    files = os.listdir(save_dir)
    count = 0
    for file in files:
        file_path = os.path.join(save_dir, file)
        file_paths.append(file_path)
        all_file_snippets[count] = extract_file_snippet(f'{save_dir}/{file}')
        file_path = os.path.join(save_dir, file)
        if os.path.isfile(file_path):
            st.write(f"📄 {file}") 
        print(f"File saved to {file_path}")

        count += 1


# Chat-like Input Section
st.subheader("Create a dashboard")
suggestion = "show me a map of Russian equipment losses filterable by type"
with st.form("chat_form"):
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    user_input = st.text_input(
        suggestion,  # Provide a label for accessibility
        placeholder=suggestion,
        label_visibility="collapsed",  # Hide the label visually
        key="chat_input",
    )
    submitted = st.form_submit_button("Let's go", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

def generate_safe_filename(input_text, max_length=20):
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

# Display the input
commonly_missed_imports = "from streamlit_folium import folium_static\n"
set_title = """import streamlit as st\nst.set_page_config(page_icon="🤖", layout="centered")\n"""

if submitted and user_input.strip():
    formatted = f"Snippet(s) of the user's files: {all_file_snippets}\nThis is their request: {user_input}\nThese are the file path(s): {file_paths}"
    with open('data/prompt_history.log', 'a') as f:
        f.write(formatted+'\n')
    response = generate_streamlit(formatted)
    format_response = response

    # Create the "pages" directory if it doesn't exist
    pages_dir = "pages"
    os.makedirs(pages_dir, exist_ok=True)

    filename = f"{generate_safe_filename(user_input)}.py"
    file_path = os.path.join(pages_dir, filename)

    # Extract dependencies from the generated code (basic regex for import statements)
    dependencies = set()
    for line in response.splitlines():
        if line.startswith("import ") or line.startswith("from "):
            dep = line.split()[1].split(".")[0]  # Extract the root module
            dependencies.add(dep)

    # Ensure all dependencies are installed
    for dep in dependencies:
        ensure_library_installed(dep)

    # Write the response to the file
    try:
        with open(file_path, "w") as f:
            f.write(f"{commonly_missed_imports}{set_title}{response}")
        st.success(f"Generated code saved to {file_path}")
    except Exception as e:
        st.error(f"Error saving file: {e}")

    # Display the raw generated code
    st.subheader("Check the left menu for your dashboard. Below is GPT-4o mini's code to create your dashboard:")
    st.code(response, language="python")
