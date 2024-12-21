import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import st_folium

# Load data
file_path = 'user_uploaded_files/russia_losses.json'
with open(file_path, 'r') as f:
    data = json.load(f)

# Convert to DataFrame
losses_df = pd.json_normalize(data['losses'])

# Filter the data
loss_type = st.selectbox("Select Type of Loss", options=losses_df['type'].unique())
filtered_df = losses_df[losses_df['type'] == loss_type]

# Initialize map
if not filtered_df.empty:
    loss_map = folium.Map(location=[48.3794, 31.1656], zoom_start=6)
    
    for index, row in filtered_df.iterrows():
        if row['geo']:  # Check if geo coordinates are available
            lat, lon = map(float, row['geo'].split(','))
            tooltip = f"Model: {row['model']}<br>Status: {row['status']}<br>Location: {row['nearest_location']}"
            folium.Marker([lat, lon], tooltip=tooltip).add_to(loss_map)
    
    st_folium(loss_map, width=700, height=500)
else:
    st.write("No data available for the selected type.")