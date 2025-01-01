import streamlit as st
st.set_page_config(page_icon="🤖", layout="centered")
from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import pydeck as pdk

# Load data
data_filepath = 'user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv'
df = pd.read_csv(data_filepath)

# Clean and preprocess data
df['lat'] = df['lat'].str.extract(r'([0-9.]+)').astype(float)
df['lon'] = df['lon'].str.extract(r'([0-9.]+)').astype(float)
df = df[df['status'] == 'Destroyed']
df_grouped = df.groupby('nearest_location_placename').agg({'id': 'count', 'lat': 'mean', 'lon': 'mean'}).reset_index()
df_grouped.rename(columns={'id': 'destroyed_count'}, inplace=True)

# Set up dashboard layout
st.title("Destroyed Vehicles by Province/Districts")

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=df_grouped['lat'].mean(),
        longitude=df_grouped['lon'].mean(),
        zoom=6,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df_grouped,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius='destroyed_count * 500',
            radius_scale=0.5,
            pickable=True,
        ),
        pdk.Layer(
            'TextLayer',
            data=df_grouped,
            pickable=True,
            get_position='[lon, lat]',
            get_text='nearest_location_placename',
            get_size=16,
            get_color='[0, 0, 0, 200]',
            get_alignment_baseline='"bottom"',
        )
    ],
))

st.write("## Data Table")
st.dataframe(df_grouped)

st.markdown("""Dashboard generated for your request: \"Can you show me a dashboard that has a map of Sum of Destroyed Vehicles by Province/Districts\" """)
st.markdown("""On data: \"02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv\" """)

        
st.markdown("""gpt-4o generated code:""")
st.code("""import streamlit as st
import pandas as pd
import pydeck as pdk

# Load data
data_filepath = 'user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv'
df = pd.read_csv(data_filepath)

# Clean and preprocess data
df['lat'] = df['lat'].str.extract(r'([0-9.]+)').astype(float)
df['lon'] = df['lon'].str.extract(r'([0-9.]+)').astype(float)
df = df[df['status'] == 'Destroyed']
df_grouped = df.groupby('nearest_location_placename').agg({'id': 'count', 'lat': 'mean', 'lon': 'mean'}).reset_index()
df_grouped.rename(columns={'id': 'destroyed_count'}, inplace=True)

# Set up dashboard layout
st.title("Destroyed Vehicles by Province/Districts")

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=df_grouped['lat'].mean(),
        longitude=df_grouped['lon'].mean(),
        zoom=6,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df_grouped,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius='destroyed_count * 500',
            radius_scale=0.5,
            pickable=True,
        ),
        pdk.Layer(
            'TextLayer',
            data=df_grouped,
            pickable=True,
            get_position='[lon, lat]',
            get_text='nearest_location_placename',
            get_size=16,
            get_color='[0, 0, 0, 200]',
            get_alignment_baseline='"bottom"',
        )
    ],
))

st.write("## Data Table")
st.dataframe(df_grouped)""", language="python")
