from kaggle_utils import download_dataset, search_datasets
import streamlit as st
from uuid import uuid4
from config import KAGGLE_API

# Initialize session state for search term and selected datasets
if "search_term" not in st.session_state:
    st.session_state.search_term = ""
if "selected_datasets" not in st.session_state:
    st.session_state.selected_datasets = set()  # Use a set for unique selections

# Search input
search_term = st.chat_input(
    placeholder="Search Kaggle datasets",
)

# Update the search term in session state
if search_term and search_term != st.session_state.search_term:
    st.session_state.search_term = search_term
    st.session_state.selected_datasets.clear()  # Clear selections for new search

# User searched
if st.session_state.search_term:
    with st.spinner(text=f"Searching for datasets matching: **{st.session_state.search_term}**"):
        try:
            # Search Kaggle datasets
            datasets = search_datasets(st.session_state.search_term)

            # Dynamically distribute datasets across columns
            num_columns = 3  # Adjust number of columns as needed
            columns = st.columns(num_columns)

            for index, dataset in enumerate(datasets):
                col = columns[index % num_columns]  # Rotate through columns
                with col.container(height=200):
                    # Display dataset title and other details
                    st.write(f"**[{dataset.title}]({dataset.url})** ^{dataset.voteCount} ({int(dataset.usabilityRating*100)}% user-friendly)")
                    # Checkbox for selection
                    checkbox_key = f"select_{dataset.ref}"
                    is_selected = checkbox_key in st.session_state.selected_datasets
                    if st.checkbox(
                        "Select for download",
                        key=checkbox_key,
                        value=is_selected,
                    ):
                        st.session_state.selected_datasets.add(dataset.ref)
                    else:
                        st.session_state.selected_datasets.discard(dataset.ref)
                    st.caption(f"{dataset.subtitle} ({dataset.size})")
                    
                    

            col1, col2, col3 = st.columns(3)
            with col2:
                # Button to download selected datasets
                if st.button("Download selected dataset(s)"):
                    if st.session_state.selected_datasets:
                        for dataset_ref in st.session_state.selected_datasets:
                            st.toast(f"Downloading dataset: {dataset_ref}")
                            download_dataset(dataset_ref, download_path="user_uploaded_files")
                        st.success(f"{dataset_ref} downloaded successfully! The files are now available in Dashboard Creator -> Select files")
                    else:
                        st.warning("No datasets selected for download.")
        except Exception as e:
            st.error(f"An error occurred while searching datasets: {e}")
