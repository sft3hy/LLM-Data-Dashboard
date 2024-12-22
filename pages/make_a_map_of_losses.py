from streamlit_folium import folium_static
import streamlit as st
st.set_page_config(page_icon="🤖", layout="centered")
import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import folium_static

# Load the JSON data
file_path = 'user_uploaded_files/russia_losses.json'
with open(file_path, 'r') as f:
    data = json.load(f)

# Flatten and load the data into a dataframe
df = pd.json_normalize(data['losses'])

# Create a Streamlit sidebar to filter by "type"
type_options = df['type'].unique()
selected_type = st.sidebar.selectbox("Filter by Type", ["All"] + list(type_options))

# Filter the dataframe based on the selected type
if selected_type != "All":
    filtered_df = df[df['type'] == selected_type]
else:
    filtered_df = df

# Create a map using Folium
m = folium.Map(location=[48.3794, 31.1656], zoom_start=6)  # Centered near Ukraine

# Loop through the filtered dataframe and add markers for entries with geo-coordinates
for _, row in filtered_df.iterrows():
    if row['geo']:
        lat, lon = map(float, row['geo'].split(','))
        tooltip = f"Type: {row['type']}<br>Model: {row['model']}<br>Status: {row['status']}<br>Date: {row['date']}<br>Location: {row['nearest_location']}"
        folium.Marker(
            location=[lat, lon],
            popup=tooltip,
            icon=folium.Icon(color='red' if row['status'] == "Destroyed" else 'blue')
        ).add_to(m)

# Render the map in Streamlit
st.title("Map of Losses")
st.subheader("Filter by Type")
folium_static(m)