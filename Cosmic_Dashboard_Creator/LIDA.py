import streamlit as st
from lida import Manager, TextGenerationConfig, llm
from lida.datamodel import Goal
import os
import json
import pandas as pd
from lida_utils import groq_generator, azure_generator
from config import GROQ_MODELS
from helpers.misc import fix_json

# make data dir if it doesn't exist
os.makedirs("data", exist_ok=True)

st.set_page_config(
    page_title="LIDA: Automatic Generation of Visualization and Infographics",
    page_icon="📊",
    layout="wide"
)

st.write("# LIDA: Automatic Generation of Visualization and Infographics using Large Language Models 📊")

st.markdown(
    """
    LIDA is a library for generating data visualizations and data-faithful infographics.
    LIDA is grammar agnostic (will work with any programming language and visualization
    libraries e.g. matplotlib, seaborn, altair, d3 etc) and works with multiple large language
    model providers (OpenAI, Azure OpenAI, PaLM, Cohere, Huggingface). Details on the components
    of LIDA are described in the [paper here](https://arxiv.org/abs/2303.02927) and in this
    tutorial [notebook](notebooks/tutorial.ipynb). See the project page [here](https://microsoft.github.io/lida/) for updates!.

   ----
""")

# Step 2 - Select a dataset and summarization method
# Initialize selected_dataset to None
selected_dataset = None

# select model from model selection
st.sidebar.write("## Text Generation Model")
models = ["gpt-4o", "gpt-4o-mini"] + GROQ_MODELS
selected_model = st.sidebar.selectbox(
    'Choose a model',
    options=models,
    index=5,
)

# select temperature on a scale of 0.0 to 1.0
# st.sidebar.write("## Text Generation Temperature")
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.5)


# Handle dataset selection and upload
st.sidebar.write("## Data Summarization")
st.sidebar.write("### Choose a dataset")

datasets = [
    {"label": "Select a dataset", "url": None},
    {"label": "Cars", "url": "https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv"},
    {"label": "Weather", "url": "https://raw.githubusercontent.com/uwdata/draco/master/data/weather.json"},
]

files_path = "user_uploaded_files"
files = [f for f in os.listdir(files_path) if os.path.isfile(os.path.join(files_path, f))]
for f in files:
    datasets.append({"label": f, "url": f"{files_path}/{f}"})

selected_dataset_label = st.sidebar.selectbox(
    'Choose a dataset',
    options=[dataset["label"] for dataset in datasets],
    index=0,
    label_visibility="collapsed"
)

upload_own_data = st.sidebar.checkbox("Upload your own data")

if upload_own_data:
    uploaded_file = st.sidebar.file_uploader("Choose a CSV or JSON file", type=["csv", "json"])

    if uploaded_file is not None:
        # Get the original file name and extension
        file_name, file_extension = os.path.splitext(uploaded_file.name)

        # Load the data depending on the file type
        if file_extension.lower() == ".csv":
            data = pd.read_csv(uploaded_file)
        elif file_extension.lower() == ".json":
            data = pd.read_json(uploaded_file)

        # Save the data using the original file name in the data dir
        uploaded_file_path = os.path.join("data", uploaded_file.name)
        data.to_csv(uploaded_file_path, index=False)

        selected_dataset = uploaded_file_path

        datasets.append({"label": file_name, "url": uploaded_file_path})

        # st.sidebar.write("Uploaded file path: ", uploaded_file_path)
else:
    selected_dataset = datasets[[dataset["label"]
                                    for dataset in datasets].index(selected_dataset_label)]["url"]

if not selected_dataset:
    st.info("To continue, select a dataset from the sidebar on the left or upload your own.")

st.sidebar.write("### Choose a summarization method")
# summarization_methods = ["default", "llm", "columns"]
summarization_methods = [
    {"label": "llm",
        "description":
        "Uses the LLM to generate annotate the default summary, adding details such as semantic types for columns and dataset description"},
    {"label": "default",
        "description": "Uses dataset column statistics and column names as the summary"},

    {"label": "columns", "description": "Uses the dataset column names as the summary"}]

# selected_method = st.sidebar.selectbox("Choose a method", options=summarization_methods)
selected_method_label = st.sidebar.selectbox(
    'Choose a method',
    options=[method["label"] for method in summarization_methods],
    index=2
)

selected_method = summarization_methods[[
    method["label"] for method in summarization_methods].index(selected_method_label)]["label"]

# add description of selected method in very small font to sidebar
selected_summary_method_description = summarization_methods[[
    method["label"] for method in summarization_methods].index(selected_method_label)]["description"]

if selected_method:
    st.sidebar.markdown(
        f"<span> {selected_summary_method_description} </span>",
        unsafe_allow_html=True)

# Step 3 - Generate data summary
if selected_dataset and selected_method:
    groq_lida = Manager(text_gen=groq_generator)
    azure_lida = Manager(text_gen=azure_generator)
    textgen_config = TextGenerationConfig(
        n=1,
        temperature=temperature,
        model=selected_model,)

    st.write("## Summary")
    # **** lida.summarize *****
    lida = ""
    if selected_model in GROQ_MODELS:
        lida = groq_lida
    else:
        lida = azure_lida
    summary = lida.summarize(
        selected_dataset,
        summary_method=selected_method,
        textgen_config=textgen_config)
    summary = json.loads(fix_json(str(summary)))
    if "dataset_description" in summary:
        st.write(summary["dataset_description"])

    if "fields" in summary:
        fields = summary["fields"]
        nfields = []
        for field in fields:
            flatted_fields = {}
            flatted_fields["column"] = field["column"]
            # flatted_fields["dtype"] = field["dtype"]
            for row in field["properties"].keys():
                if row != "samples":
                    flatted_fields[row] = field["properties"][row]
                else:
                    flatted_fields[row] = str(field["properties"][row])
            # flatted_fields = {**flatted_fields, **field["properties"]}
            nfields.append(flatted_fields)
        nfields_df = pd.DataFrame(nfields)
        st.write(nfields_df)
    else:
        st.write(str(summary))
    # Cache the goal generation function
    @st.cache_data(show_spinner=True)
    def generate_goals(summary, num_goals, textgen_config):
        return lida.goals(summary, n=num_goals, textgen_config=textgen_config)

    # Goal selection section
    if summary:
        st.sidebar.write("### Goal Selection")

        # Slider for number of goals to generate
        num_goals = st.sidebar.slider(
            "Number of goals to generate",
            min_value=1,
            max_value=10,
            value=4
        )

        # Checkbox to add a custom goal
        own_goal = st.sidebar.checkbox("Add Your Own Goal")

        # Generate goals using the cached function
        goals = generate_goals(summary, num_goals, textgen_config)
        goal_questions = [goal.question for goal in goals]

        # Allow user to add a custom goal
        if own_goal:
            user_goal = st.sidebar.text_input("Describe Your Goal")
            if user_goal:
                new_goal = Goal(question=user_goal, visualization=user_goal, rationale="")
                goals.append(new_goal)
                goal_questions.append(new_goal.question)

        # Select a goal without regenerating goals
        selected_goal = st.selectbox(
            'Choose a visualization goal',
            options=goal_questions,
            index=0,
            key="selected_goal"  # Use a unique key to maintain state
        )

        # Display the selected goal details
        selected_goal_index = goal_questions.index(selected_goal)
        st.write(goals[selected_goal_index])

        selected_goal_object = goals[selected_goal_index]

        # Step 5 - Generate visualizations
        if selected_goal_object:
            
            # Update the visualization generation call to use the selected library.
            st.write("## Visualizations")

            # slider for number of visualizations
            num_visualizations = st.sidebar.slider(
                "Number of visualizations to generate",
                min_value=1,
                max_value=10,
                value=2)
            
            st.sidebar.write("## Visualization Library")
            visualization_libraries = ["seaborn", "matplotlib", "plotly"]

            selected_library = st.sidebar.selectbox(
                'Choose a visualization library',
                options=visualization_libraries,
                index=0,
                label_visibility="collapsed"
            )

            textgen_config = TextGenerationConfig(
                n=num_visualizations, temperature=temperature,
                model=selected_model,)

            # **** lida.visualize *****
            visualizations = lida.visualize(
                summary=summary,
                goal=selected_goal_object,
                textgen_config=textgen_config,
                library=selected_library)

            viz_titles = [f'Visualization {i+1}' for i in range(len(visualizations))]
            print('VIZ_TITLES', viz_titles)
            if viz_titles != []:
                selected_viz_title = st.selectbox('Choose a visualization', options=viz_titles, index=0)

                selected_viz = visualizations[viz_titles.index(selected_viz_title)]

                if selected_viz.raster:
                    from PIL import Image
                    import io
                    import base64

                    imgdata = base64.b64decode(selected_viz.raster)
                    img = Image.open(io.BytesIO(imgdata))
                    st.image(img, caption=selected_viz_title, use_column_width=True)

                st.write("### Visualization Code")
                st.code(selected_viz.code)
            else:
                st.error("Error creating visualization, try a different goal.")