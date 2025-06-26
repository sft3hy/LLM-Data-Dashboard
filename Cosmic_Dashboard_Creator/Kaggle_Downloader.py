import streamlit as st
from uuid import uuid4
from utils.kaggle_utils import download_dataset, search_datasets
from streamlit_extras.tags import tagger_component

# Initialize session state for search term and selected datasets
if "search_term" not in st.session_state:
    st.session_state.search_term = ""
if "selected_datasets" not in st.session_state:
    st.session_state.selected_datasets = set()  # Use a set for unique selections

# Search input
search_term = st.text_input(
    "Search for Kaggle datasets",
    placeholder="Try something like 'heart health'",
)

# Display initial instructions
search_info_container = st.empty()
search_info_container.markdown("**Search for datasets to download from Kaggle**")

# Update the search term in session state
if search_term and search_term != st.session_state.search_term:
    st.session_state.search_term = search_term
    st.session_state.selected_datasets.clear()  # Clear selections for new search

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
                    st.write(f"**[{dataset.title}]({dataset.url})**")
                    st.write(f"👍 {dataset.voteCount} | Usability: {int(dataset.usabilityRating * 100)}%")

                    # Checkbox to select datasets
                    checkbox_key = f"select_{dataset.ref}"
                    is_selected = dataset.ref in st.session_state.selected_datasets
                    if st.checkbox(
                        "Select for download",
                        key=checkbox_key,
                        value=is_selected,
                    ):
                        st.session_state.selected_datasets.add(dataset.ref)
                    else:
                        st.session_state.selected_datasets.discard(dataset.ref)

                    st.caption(f"{dataset.subtitle} ({dataset.size})")
                    tagger_component(dataset.tags, color_names[:len(dataset.tags)])

            # Button to download selected datasets
            if st.button("Download selected dataset(s)"):
                if st.session_state.selected_datasets:
                    for dataset_ref in st.session_state.selected_datasets:
                        st.toast(f"Downloading dataset: {dataset_ref}")
                        download_dataset(dataset_ref, download_path="user_uploaded_files")
                    st.success("Datasets downloaded successfully!")
                else:
                    st.warning("No datasets selected for download.")
        except Exception as e:
            st.error(f"An error occurred while searching datasets: {e}")
