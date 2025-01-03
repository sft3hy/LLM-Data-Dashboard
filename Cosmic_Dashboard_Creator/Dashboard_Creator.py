import streamlit as st
import os
import time
from helpers.model_caller import call_model
from helpers.parse_file import extract_file_snippet, preview_file
from helpers.dependency_ensurer import ensure_library_installed
from helpers.misc import is_directory_empty, generate_safe_filename, extract_message, get_new_filename
from helpers.code_editor import correct_code
from refiner_bar import output_refined_dashboard
from config import GROQ_MODELS, streamlit_sys_prompt


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
    with col2:
        file_preview = st.checkbox(
            "Show file previews"
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

        st.subheader('Or select from previously uploaded:')


        # Dropdown with checkboxes
        with st.expander("Select Files", expanded=False):
            files = os.listdir(save_dir)
            for count, file in enumerate(files):
                file_path = os.path.join(save_dir, file)
                file_paths.append(file_path)
                file_snippet = preview_file(file_path)
                all_file_snippets[file_path] = file_snippet
                
                if os.path.isfile(file_path):
                    # Add a checkbox for each file
                    is_selected = st.checkbox(f"📄 {file}", key=f"file_{count}")
                    if is_selected:
                        selected_files.append(file_path)
                    if file_preview:
                        st.write(f"Columns: {file_snippet['columns']}")
                        st.write(f"Number of rows: {file_snippet['num_rows']}")
                        st.write(' ')

                    
                    
                    # # Add a preview button for each file
                    # with st.container():
                    #     st.write(f"**File:** {file}")
                    #     st.write(f"**Columns:** {file_snippet['columns']}")
                    #     st.write(f"**Number of Rows:** {file_snippet['num_rows']}")
                
                    


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


if submitted and user_input.strip() and selected_files and selected_model:
    formatted = f"Snippet(s) of the user's files: {all_file_snippets}\nThis is their request: {user_input}\nThese are the file path(s): {selected_files}"
    response = call_model(model_name=selected_model, gpt_request=formatted, system_prompt=streamlit_sys_prompt)
    format_response = extract_message(response)

    # Create the "pages" directory if it doesn't exist
    pages_dir = "Your_Dashboards"
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
    pretty_name = 'ERROR'
    try:
        files = ', '.join([os.path.basename(f) for f in selected_files])
        commonly_missed_imports = "from streamlit_folium import folium_static\nfrom streamlit_folium import st_folium\n"

        page_config_robot = f"""import streamlit as st\nst.set_page_config(page_icon="🤖", layout="centered")\n"""

        maybe_correct = correct_code(code_snippet=f"{page_config_robot}{commonly_missed_imports}{response}", extra_context=formatted)

        user_requests = f"""
# Dashboard generated for your request: \"{user_input}\"
# On data: \"{files}\"\n
"""
        hidden_code_info = f"""
with st.expander("View {selected_model} streamlit dashboard code"):
    st.code(\"\"\"{user_requests}{maybe_correct}\"\"\", language="python")
"""
        filename_info = get_new_filename(maybe_correct)
        if filename_info is None:
            filename_to_write = file_path
            pretty_name = filename.replace('_', ' ').replace('.py', '')
        else:
            filename_to_write = filename_info['full_filename']
            pretty_name = filename_info['pretty_name']
        gimme_more = output_refined_dashboard(maybe_correct)
        with open(filename_to_write, "w") as f:
            f.write(f"{page_config_robot}{commonly_missed_imports}{maybe_correct}{hidden_code_info}{gimme_more}")
    except Exception as e:
        st.error(f"Error saving file: {e}")

    st.subheader(f"Your new dashboard will be named \"{pretty_name}\" in the left menu bar. Refresh this page to view it.")

    

