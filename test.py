from helpers.code_corrector import correct_code

context = """Snippet(s) of the user's files: {'user_uploaded_files/russia_losses.json': '{\n  "losses": [\n    {\n      "id": 32731,\n      "type": "Infantry fighting vehicles",\n      "model": "BMP-3",\n      "status": "Destroyed",\n      "lost_by": "Russia",\n      "date": "2024-11-30",\n      "nearest_location": "Pershotravneve (Borova hromada), Izium raion",\n      "geo": null,\n      "unit": null,\n      "tags": "Cope cage, Jammer"\n    },\n    {\n      "id": 32730,\n      "type": "Infantry fighting vehicles",\n      "model": "BMP-1AM 675-sb3KDZ",\n      "status": "Destroyed",\n      "lost_by": "Russia",\n      "date": "2024-12-21",\n      "nearest_location": "Sukhi Yaly, Pokrovsk raion",\n      "geo": null,\n      "unit": null,\n      "tags": "Cope cage"\n    },\n    {\n      "id": 32729,\n      "type": "Infantry fighting vehicles",\n      "model": "BMD-2",\n      "status": "Abandoned",\n      "lost_by": "Russia",\n      "date": "2024-12-21",\n      "nearest_location": "Darino, Sudzha raion",\n      "geo": "51.267278,35.031333",\n      "unit": null,\n      "tags": "Cope cage"\n    },\n    {\n      "id": 3'}"""
code_snip = """python

from streamlit_folium import folium_static

import streamlit as st
import json

# Load the data from the user's file
user_uploaded_file = st.file_uploader('Select a file:', type=['json'])
if user_uploaded_file is not None:
    data = json.load(user_uploaded_file)

    # Filter the data to only include entries with the "cope cage" tag
    cope_cage_data = [entry for entry in data['losses'] if 'cope cage' in entry['tags']]

    # Display the number of losses with the "cope cage" tag
    st.header('Number of Losses with "Cope Cage" Tag')
    st.write(len(cope_cage_data))

    # Display a bar chart of the number of losses with the "cope cage" tag over time
    st.header('Number of Losses with "Cope Cage" Tag Over Time')
    dates = [entry['date'] for entry in cope_cage_data]
    counts = [1 for _ in cope_cage_data]
    st.bar_chart({"data": counts, "x": dates})

    # Display a table of the losses with the "cope cage" tag
    st.header('Losses with "Cope Cage" Tag')
    st.write(cope_cage_data)
"""

print(correct_code(code_snip, context))