import streamlit as st
import os
from datetime import datetime
from helpers.model_caller import call_model
from helpers.parse_file import extract_file_snippet, preview_file
from helpers.dependency_ensurer import ensure_library_installed
from helpers.misc import is_directory_empty, generate_safe_filename, clean_set_page_config, get_new_filename, choose_text_generator, parse_model_response
from helpers.code_editor import correct_code
from refiner_bar import output_refined_dashboard
from config import GROQ_MODELS, OPENAI_MODELS, GOOGLE_MODELS, streamlit_sys_prompt, get_now
from lida_utils import CustomTextGenerator, TextGenerationConfig

# st.set_page_config("Dashboard Creator", layout="centered")

# Title
st.title("Dashboard Creator")
save_dir = "user_uploaded_files"


# Create a container at the top of the page
top_container = st.container(border=True)


# Use columns to position the selectbox
with top_container:
    selected_model = st.selectbox(
        "Select an LLM for code generation:",
        options = OPENAI_MODELS + GOOGLE_MODELS + GROQ_MODELS,
        # label_visibility='collapsed'
    )
        


file_paths = []
all_file_snippets = {}
selected_files = []

bottom_container = st.container(border=True)

# File Upload Section
with bottom_container:

    uploaded_files = st.file_uploader(
        "Upload new file(s)",
        type=["kml", "geojson", "json", "csv", "zip"],  # Shapefiles are usually uploaded as zipped archives
        accept_multiple_files=True,
        key="main-file-uploader",
    )
    if uploaded_files and not is_directory_empty(save_dir):
        for uploaded_file in uploaded_files:
            # Save uploaded files
            os.makedirs(save_dir, exist_ok=True)
            file_path = os.path.join(save_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            selected_files.append(file_path)  # Treat uploaded files as selected


    # Dropdown with checkboxes
    file_preview = st.checkbox(
            "Show file information"
        )
    with st.expander("Or select previous data sources:", expanded=False):
        files = os.listdir(save_dir)
        for count, file in enumerate(files):
            file_path = os.path.join(save_dir, file)
            file_paths.append(file_path)
            preview_snip = preview_file(file_path)
            file_snippet = extract_file_snippet(file_path)
            
            if os.path.isfile(file_path):
                # Add a checkbox for each file
                is_selected = st.checkbox(f"📄 {file}", key=f"file_{count}")
                if is_selected:
                    selected_files.append(file_path)
                    all_file_snippets[file_path] = file_snippet
                
                if file_preview:
                    if 'error' in preview_snip.keys():
                        st.write('Error generating file preview')
                    else:
                        st.write(f"Columns: {preview_snip['columns']}")
                        st.write(f"Number of rows: {preview_snip['num_rows']}")
                        st.write(' ')
            

# Disable the button if no files are selected
# Add text input for dashboard creation
user_input = st.chat_input("What do you want your dashboard to look like?")
if user_input:
    if not selected_files:
        st.error("You must either upload new files or select existing files before creating a dashboard!")
    elif not user_input.strip():
        st.error("Please provide input for creating a dashboard!")
    elif not selected_model:
        st.error("Please select a model to create your dashboard!")
    else:
        st.success(f"Creating dashboard: '{user_input}'\n on data: '{', '.join([os.path.basename(f) for f in selected_files])}'")


else:
    pass
    # st.info("No files have been uploaded yet.")

# select temperature on a scale of 0.0 to 1.0
temperature = st.sidebar.slider(
    "Model Temperature",
    min_value=0.0,
    max_value=0.4,
    value=0.2)


if selected_files and user_input and user_input.strip() and selected_files and selected_model:
    textgen_config = TextGenerationConfig(
        n=1,
        temperature=temperature,
        model=selected_model,)
    formatted = f"Snippet(s) of the user's files: {all_file_snippets}\nThis is their request: {user_input}\nThese are the file path(s): {selected_files}"

    text_gen = choose_text_generator(selected_model)
    original_streamlit_try_messages = [
            {"role": "system", "content": streamlit_sys_prompt},
            {"role": "user",
             "content":
             f"{formatted}"}]

    result = text_gen.generate(messages=original_streamlit_try_messages, config=textgen_config)

    # response = call_model(model_name=selected_model, gpt_request=formatted, system_prompt=streamlit_sys_prompt)
    response = parse_model_response(result)
    # format_response = extract_message(response[0])
    print(response)
    # Create the "pages" directory if it doesn't exist
    pages_dir = "Your_Dashboards"
    os.makedirs(pages_dir, exist_ok=True)

    filename = f"{generate_safe_filename(user_input)}.py"
    file_path = os.path.join(pages_dir, filename)

    # Extract dependencies from the generated code (basic regex for import statements)
    dependencies = set()
    for line in response[0].splitlines():
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

        page_config_robot = "import streamlit as st\n"
        if "st.set_page_config" not in response:
            page_config_robot = f"""import streamlit as st\nst.set_page_config(page_icon="🤖", layout="centered")\n"""
        maybe_correct = correct_code(code_snippet=response, extra_context=formatted)
        whole_code = clean_set_page_config(f"{page_config_robot}{commonly_missed_imports}{maybe_correct}")

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
        gimme_more = output_refined_dashboard(maybe_correct, f"\nSnippet(s) of the user's files: {str(all_file_snippets).replace('{', '').replace('}', '')}\nThese are the file path(s): {selected_files}")
        dash_gen_time = get_now()
        optional_creator = ""
        if 'user_info' in st.session_state and st.session_state.user_info and st.session_state.user_info['name']:
            optional_creator = f" by {st.session_state.user_info['name']}"
        dash_info = f"""
st.caption(f"Dashboard created at {dash_gen_time}{optional_creator}")
"""
        with open(filename_to_write, "w") as f:
            f.write(f"{whole_code}{hidden_code_info}{dash_info}{gimme_more}")
    except Exception as e:
        st.error(f"Error saving file: {e}")

    st.subheader(f"Your new dashboard will be named \"{pretty_name}\" in the left menu bar. Refresh this page to view it.")

    

