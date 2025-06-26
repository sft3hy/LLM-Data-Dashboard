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
    value=st.session_state.search_term
)

# Display initial instructions
search_info_container = st.empty()
if not search_term:
    search_info_container.markdown("**Search for datasets to download from Kaggle**")

# Update the search term in session state
if search_term and search_term != st.session_state.search_term:
    st.session_state.search_term = search_term
    st.session_state.selected_datasets.clear()  # Clear selections for new search

color_names = ['lightblue', 'orange', 'bluegreen', 'blue', 'violet', 'red', 'green', 'yellow']
import streamlit as st

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
                    # Create a container for each dataset with a rounded box and white border
                    dataset_container = st.container()
                    with dataset_container:
                        st.markdown(
                            """
                            <div style="border: 1px solid white; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                            """,
                            unsafe_allow_html=True,
                        )

                        # Ensure dataset.title and dataset.url exist before trying to display them
                        if hasattr(dataset, 'title') and hasattr(dataset, 'url'):
                            st.write(f"**[{dataset.title}]({dataset.url})**")
                        elif hasattr(dataset, 'title'):
                            st.write(f"**{dataset.title}**")
                        else:
                            st.write("Untitled Dataset")

                        # Display vote count and usability rating if they exist
                        display_text = []
                        if hasattr(dataset, 'voteCount'):
                            display_text.append(f"👍 {dataset.voteCount}")
                        if hasattr(dataset, 'usabilityRating'):
                            usability_rating = int(getattr(dataset, 'usabilityRating', 0) * 100)
                            display_text.append(f"Usability: {usability_rating}%")
                        if display_text:
                            st.write(", ".join(display_text))  # Modified to display text in a single line

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

                        st.markdown("</div>", unsafe_allow_html=True)

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