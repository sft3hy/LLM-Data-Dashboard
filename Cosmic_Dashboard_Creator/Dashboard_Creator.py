import streamlit as st
import os
import json
from utils.model_caller import call_model
from utils.parse_file import extract_file_snippet, preview_file
from utils.dependency_ensurer import ensure_library_installed
from utils.misc import is_directory_empty, generate_safe_filename, clean_set_page_config, get_new_filename, choose_text_generator, fix_json, correct_code_remotely, wait_for_file, generate_pages, add_python_comments
from utils.code_editor import correct_code
from utils.refiner_bar import output_refined_dashboard
from config import ALL_MODELS, streamlit_sys_prompt, get_now
from lida import TextGenerationConfig, Manager
from custom_components.custom import gen_copy_button
import streamlit as st
import streamlit.components.v1 as components
from utils.message_utils import add_user_message, add_assistant_message
import time



# Title
st.title("Dashboard Creator")
save_dir = "user_uploaded_files"


# Create a container at the top of the page
top_container = st.container(border=True)


# Use columns to position the selectbox
with top_container:
    col1, col2 = st.columns(2)

    with col1:
        selected_model = st.selectbox(
            "LLM for code generation:",
            options = ALL_MODELS,
            index=ALL_MODELS.index("llama-3.3-70b-specdec"),
            # label_visibility='collapsed'
        )
    with col2:
        # select temperature on a scale of 0.0 to 0.4
        st.markdown("LLM Temperature", help="Set the model temperature. 0 = more logical, 0.4 = more creative")

        temperature = st.slider(
            "A",
            min_value=0.0,
            max_value=0.4,
            value=0.2,
            label_visibility="collapsed",
            )
        


file_paths = []
all_file_snippets = {}
selected_files = []

bottom_container = st.container(border=True)

# File Upload Section
with bottom_container:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_files = st.file_uploader(
            "Upload new file(s)",
            type=["kml", "geojson", "json", "csv", "zip"],  # Shapefiles are usually uploaded as zipped archives
            accept_multiple_files=True,
            key="main-file-uploader",
            label_visibility="collapsed"
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
    with st.expander("Or select uploaded data sources:", expanded=False):
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



if selected_model:
    textgen_config = TextGenerationConfig(
            n=1,
            temperature=temperature,
            model=selected_model,)
    lida_generator = choose_text_generator(selected_model)
    lida = Manager(text_gen=lida_generator)

if selected_files:
    col1, col2 = st.columns(2)

    with col1:
        st.write("Not sure what to ask for? Try the goal generation button to have your selected llm review your data and give you some ideas.")
        goal_generation = st.button("Generate goals")
        # summarization_methods = ["default", "llm", "columns"]
    summarization_methods = [
        {"label": "llm",
            "description":
            "Uses the LLM to parse your data and pass enriched information to the goal generator"},
        {"label": "default",
            "description": "Passes dataset column statistics and column names to the goal generator"},

        {"label": "columns", "description": "Passes the dataset column names to the goal generator"}]

    with col2:
        selected_method_label = st.selectbox(
            'Choose a goal generation method',
            options=[method["label"] for method in summarization_methods],
            index=1
        )

        selected_method = summarization_methods[[
            method["label"] for method in summarization_methods].index(selected_method_label)]["label"]

        # add description of selected method in very small font to sidebar
        selected_summary_method_description = summarization_methods[[
            method["label"] for method in summarization_methods].index(selected_method_label)]["description"]
        
        if selected_method:
            st.markdown(
                f"<span> {selected_summary_method_description} </span>",
                unsafe_allow_html=True)
    
    if goal_generation:
        with st.spinner(text="Generating goals..."):
        # Generate goals using the cached function
            for selected_file in selected_files:
                with st.spinner(text="Summarizing data set..."):
                    summary = lida.summarize(
                        selected_file,
                        summary_method=selected_method if selected_method else "columns",
                        textgen_config=textgen_config,
                        )
                    summary = json.loads(fix_json(str(summary)))

                goals = lida.goals(summary, n=6, textgen_config=textgen_config)
                goal_questions = [goal.question for goal in goals]
                st.write(f"{selected_file.split('/')[-1]} Goal Recommendations:")

                # Rotate through columns and add questions with bordered containers
                for idx, question in enumerate(goal_questions):
                    # Display the question
                    with st.container(border=True):
                        cur_goal = goals[idx]
                        goal_info = f"Question: {cur_goal.question}\nVisualization: {cur_goal.visualization}\nRationale: {cur_goal.rationale}"
                        cur_goal = goals[idx]
                        st.subheader(f"Goal {idx+1}")
                        st.write(f"Question: {cur_goal.question}")
                        st.write(f"Visualization: {cur_goal.visualization}")
                        st.write(f"Rationale: {cur_goal.rationale}")
                        components.html(gen_copy_button(goal_info), height=60)

           

if selected_files and user_input and user_input.strip() and selected_files and selected_model:
    with st.spinner("Generating Dashboard..."):
        formatted = f"Snippet(s) of the user's files: {all_file_snippets}\nThis is their request: {user_input}\nThese are the file path(s): {selected_files}"
        response = call_model(
            model_name=selected_model,
            gpt_request=formatted,
            system_prompt=streamlit_sys_prompt,
            temperature=temperature
            )
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
            maybe_correct = correct_code_remotely(code_snippet=response, extra_context=formatted, file_name="")
            whole_code = clean_set_page_config(f"{commonly_missed_imports}{maybe_correct}")

            user_requests = f"""# Dashboard generated for your request: \"{user_input}\"\n# On data: \"{files}\"\n"""
            hidden_code_info = f"View {selected_model} streamlit dashboard code"
            filename_info = get_new_filename(maybe_correct)
            if filename_info is None:
                filename_to_write = file_path
                pretty_name = filename.replace('_', ' ').replace('.py', '')
            else:
                filename_to_write = filename_info['full_filename']
                pretty_name = filename_info['pretty_name']
            gimme_more = output_refined_dashboard(f"\nSnippet(s) of the user's files: {str(all_file_snippets).replace('{', '').replace('}', '')}\nThese are the file path(s): {selected_files}")
            dash_gen_time = get_now()
            optional_creator = ""
            if 'user_info' in st.session_state and st.session_state.user_info and st.session_state.user_info['name']:
                optional_creator = f" by {st.session_state.user_info['name']}"
            dash_info = f"dashboard created at {dash_gen_time}{optional_creator}"
            only_filename = filename_to_write.split('/')[-1]
            add_user_message(only_filename, message_contents=user_input, user_id=optional_creator)
            add_assistant_message(only_filename,
                                  message_contents=f"{selected_model} {dash_info}",
                                  assistant_code_expander=hidden_code_info,
                                  assistant_code_top=add_python_comments(user_requests),
                                  assistant_code=f"{whole_code}",
                                  )
            with open(filename_to_write, "w") as f:
                f.write(page_config_robot + gimme_more)
        except Exception as e:
            st.error(f"Error saving file: {e}")
    with st.spinner('Writing file...'):
        if wait_for_file(filename_to_write):
            dashboard_pages = generate_pages()
            # Page configuration
            creator = st.Page(
                "Cosmic_Dashboard_Creator/Dashboard_Creator.py", title="Dashboard Creator", icon=":material/dashboard:", default=True, 
            )
            about = st.Page(
                "Cosmic_Dashboard_Creator/About.py", title="About", icon=":material/waving_hand:",
            )
            model_info = st.Page(
                "Cosmic_Dashboard_Creator/Model_Information.py", title="Model Info", icon=":material/info:"
            )
            kaggle = st.Page(
                "Cosmic_Dashboard_Creator/Kaggle_Downloader.py", title="Kaggle Downloader", icon="🦆"
            )
            lida = st.Page(
                "Cosmic_Dashboard_Creator/LIDA.py", title="LIDA", icon="📊"
            )

            pg = st.navigation(
            {
                "Cosmic Dashboard Creator": [creator, about, model_info, kaggle, lida],
                "Your Dashboards": dashboard_pages,
            }
            )
            st.write("Go to your new dashboard")
            st.page_link(filename_to_write, label=pretty_name, icon="🤖")

    

