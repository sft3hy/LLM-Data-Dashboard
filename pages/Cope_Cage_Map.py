from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import json
import pydeck as pdk

# Load data
with open('user_uploaded_files/russia_losses.json') as f:
    data = json.load(f)

# Convert data to DataFrame
df = pd.json_normalize(data['losses'])

# Filter data for "Cope cage" in tags and entries with geo coordinates
df['tags'] = df['tags'].fillna('')
df_filtered = df[df['tags'].str.contains('Cope cage') & df['geo'].notnull()]

# Split geo coordinates into latitude and longitude
df_filtered[['latitude', 'longitude']] = df_filtered['geo'].str.split(',', expand=True).astype(float)

# Streamlit app
st.title("Cope Cage Map")

if not df_filtered.empty:
    # Create a map visualization
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=df_filtered['latitude'].mean(),
            longitude=df_filtered['longitude'].mean(),
            zoom=6,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df_filtered,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=10000,
                pickable=True
            )
        ],
        tooltip={
            "html": "<b>Type:</b> {type} <br/><b>Model:</b> {model} <br/><b>Status:</b> {status} <br/><b>Location:</b> {nearest_location}",
            "style": {"color": "white"}
        }
    ))
else:
    st.write("No data with 'Cope cage' and geo coordinates available.")