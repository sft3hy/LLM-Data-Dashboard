import streamlit as st
from uuid import uuid4
from utils.kaggle_utils import download_dataset, search_datasets
from streamlit_extras.tags import tagger_component

# Initialize session state for search term and selected datasets
if "search_term" not in st.session_state:
    st.session_state.search_term = ""
if "selected_datasets" not in st.session_state:
    st.session_state.selected_datasets = set()  # Use a set for unique selections

# **Updated Search Input Logic**
search_input = st.text_input(
    "Search for Kaggle datasets",
    placeholder="Try something like 'heart health'",
    value=st.session_state.search_term,
    key="search_input"
)

# Only update the session state if the text input changes
if search_input != st.session_state.search_term:
    st.session_state.search_term = search_input
    st.session_state.selected_datasets.clear()  # Clear previous selections for new searches

# Display initial instructions
search_info_container = st.empty()
if not st.session_state.search_term:
    search_info_container.markdown("**Search for datasets to download from Kaggle**")

color_names = ['lightblue', 'orange', 'bluegreen', 'blue', 'violet', 'red', 'green', 'yellow']

# Process user search
if st.session_state.search_term:
    with st.spinner(f"Searching for datasets matching: **{st.session_state.search_term}**"):
        try:
            datasets = search_datasets(st.session_state.search_term)

            # Hide the search info container when datasets are found
            search_info_container.empty()

            # Dynamically distribute datasets across columns
            num_columns = 3
            columns = st.columns(num_columns)

            for index, dataset in enumerate(datasets):
                col = columns[index % num_columns]
                with col:
                    # Create a container for each dataset with a styled box
                    with st.container():
                        # Use Markdown to create the styled box for the dataset
                        st.markdown(
                            f"""<div style="border:1px solid white; border-radius:10px; padding:10px; margin-bottom:10px; background-color:#03216f;"><h4 style="margin-top:0px;">{getattr(dataset, 'title', 'Untitled Dataset')}</h4>{f'<a href="{getattr(dataset, "url", "#")}" target="_blank">View Dataset</a>' if hasattr(dataset, "url") else "No URL available"}{f"👍 {getattr(dataset, 'voteCount', 0)} votes" if hasattr(dataset, 'voteCount') else ''}{f", Usability: {int(getattr(dataset, 'usabilityRating', 0) * 100)}%" if hasattr(dataset, 'usabilityRating') else ''}</div>""",
                            unsafe_allow_html=True,
                        )

                        # Checkbox to select datasets
                        checkbox_key = f"select_{getattr(dataset, 'ref', 'unknown')}"
                        is_selected = st.checkbox(
                            "Select for download",
                            key=checkbox_key,
                            value=getattr(dataset, 'ref', None) in st.session_state.selected_datasets
                        )
                        if is_selected:
                            st.session_state.selected_datasets.add(getattr(dataset, 'ref', 'unknown'))
                        else:
                            st.session_state.selected_datasets.discard(getattr(dataset, 'ref', 'unknown'))

            # Download button for selected datasets
            if st.button("Download selected dataset(s)"):
                if st.session_state.selected_datasets:
                    for dataset_ref in st.session_state.selected_datasets:
                        st.toast(f"Downloading dataset: {dataset_ref}")
                        download_dataset(dataset_ref, download_path="user_uploaded_files")
                    st.success("Datasets downloaded successfully!")
                else:
                    st.warning("No datasets selected for download.")
        except Exception as e:
            st.error(f"An error occurred: {e}")