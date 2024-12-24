import streamlit as st
import os
from helpers.model_caller import call_model
from helpers.parse_file import extract_file_snippet
from helpers.dependency_ensurer import ensure_library_installed
from helpers.misc import is_directory_empty, generate_safe_filename, extract_message
from helpers.code_corrector import correct_code
from config import GROQ_MODELS, streamlit_sys_prompt

# Page configuration
st.set_page_config(page_title="Dashboard Creator", page_icon="📊", layout="centered")


# Title
st.title("Dashboard Creator")
save_dir = "user_uploaded_files"


# Create a container at the top of the page
top_container = st.container()


# Use columns to position the selectbox
with top_container:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        selected_model = st.selectbox(
            "Select an LLM for code generation:",
            options=['gpt-4o', 'gpt-4o-mini'] + GROQ_MODELS,
            # label_visibility='collapsed'
        )


file_paths = []
all_file_snippets = {}
selected_files = []

if not is_directory_empty(save_dir):
    # Initialize variables for selected files and input
    suggestion = "show me a map of Russian equipment losses filterable by type"

    # Create a form for both file selection and text input
    with st.form("selection_and_input_form"):

        # File Upload Section
        st.subheader("Either upload new files:")

        uploaded_files = st.file_uploader(
            "A",
            type=["kml", "geojson", "json", "csv", "zip"],  # Shapefiles are usually uploaded as zipped archives
            accept_multiple_files=True,
            label_visibility="collapsed",  # Completely hide the label

        )
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Save uploaded files
                os.makedirs(save_dir, exist_ok=True)
                file_path = os.path.join(save_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                selected_files.append(file_path)  # Treat uploaded files as selected

        st.subheader('Or select previously uploaded data files:')

        # Display files with checkboxes
        files = os.listdir(save_dir)
        for count, file in enumerate(files):
            file_path = os.path.join(save_dir, file)
            file_paths.append(file_path)
            all_file_snippets[file_path] = extract_file_snippet(file_path)
            if os.path.isfile(file_path):
                # Add a checkbox for each file
                is_selected = st.checkbox(f"📄 {file}", key=f"file_{count}")
                if is_selected:
                    selected_files.append(file_path)
        # Add text input for dashboard creation
        st.subheader("Your dashboard request:")
        user_input = st.text_input(
            suggestion,  # Provide a label for accessibility
            placeholder=suggestion,
            label_visibility="collapsed",  # Hide the label visually
            key="chat_input",
        )
        

        # Add a single "Let's Go" button for submission
        submitted = st.form_submit_button("Let's Go", type="primary")

        # Disable the button if no files are selected
        if submitted:
            if not selected_files:
                st.error("You must either upload new files or select existing files before creating a dashboard!")
            elif not user_input.strip():
                st.error("Please provide input for creating a dashboard!")
            elif not selected_model:
                st.error("Please select a model to create your dashboard!")
            else:
                st.success(f"Creating dashboard: '{user_input}'\n on data: '{', '.join([os.path.basename(f) for f in selected_files])}'")


else:
    st.info("No files have been uploaded yet.")


# Display the input
if submitted and user_input.strip() and selected_files and selected_model:
    formatted = f"Snippet(s) of the user's files: {all_file_snippets}\nThis is their request: {user_input}\nThese are the file path(s): {selected_files}"
    with open('data/prompt_history.log', 'a') as f:
        f.write(formatted+'\n'+'Using model: '+selected_model+'\n')
    # response = "st.write('ayo')"
    response = call_model(model_name=selected_model, gpt_request=formatted, system_prompt=streamlit_sys_prompt)
    format_response = extract_message(response)

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
        maybe_correct = correct_code(code_snippet=response, extra_context=formatted)
        files = ', '.join([os.path.basename(f) for f in selected_files])
        commonly_missed_imports = "from streamlit_folium import folium_static\n"
        page_config_robot = f"""import streamlit as st\nst.set_page_config(page_icon="🤖", layout="centered")\n"""
        user_requests = f"""

st.markdown(\"\"\"Dashboard generated for your request: \\"{user_input}\\" \"\"\")
st.markdown(\"\"\"On data: \\"{files}\\" \"\"\")
"""
        hidden_code_info = f"""
        
st.markdown(\"\"\"{selected_model} generated code:\"\"\")
st.code(\"\"\"{maybe_correct}\"\"\", language="python")
"""
        with open(file_path, "w") as f:
            f.write(f"{page_config_robot}{commonly_missed_imports}{maybe_correct}{user_requests}{hidden_code_info}")
    except Exception as e:
        st.error(f"Error saving file: {e}")

    # Display the raw generated code
    st.subheader(f"Check the left menu to view your dashboard and the code that created it.")
    

