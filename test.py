import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard

with open("data/resources/content_copy.svg", "r") as copy:
    copy_svg = copy.read()


goals_raw = """What is the geographic distribution of vehicle losses based on their coordinates?
What are the trends in vehicle losses over time?
What are the most common vehicle types and models involved in losses?
What is the relationship between vehicle status and tags?
Which locations (nearest_location_placename) have the highest frequency of vehicle losses?
What is the relationship between vehicle status and tags?"""

selected_files = ['user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv']
goal_generation = st.button("Generate goals")
if goal_generation:
    with st.spinner(text="Generating goals..."):
        # Generate goals using the cached function
        for selected_file in selected_files:
            goal_questions = goals_raw.split('\n')
            st.write(f"{selected_file.split('/')[-1]} Goal Recommendations:")
            
            # Adjust number of columns as needed
            num_columns = 3
            columns = st.columns(num_columns)

            # Rotate through columns and add questions with bordered containers
            for idx, question in enumerate(goal_questions):
                col = columns[idx % num_columns]  # Rotate through columns
                with col.container(height=150, border=True):
                    # Display the question
                    st.write(question)
                    st_copy_to_clipboard(question,
                                         key=str(idx),
                                         after_copy_label="Copied!"
                                         )



