import streamlit as st
st.set_page_config(page_icon="🤖", layout="centered")
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import streamlit as st
import pandas as pd
import plotly.express as px

# Title for the app
st.title("Geospatial Analysis of Vehicle Losses with Map Animation")

# Load the data
file_path = 'user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv'
data = pd.read_csv(file_path, skipinitialspace=True)

# Convert date column to datetime format
data['date'] = pd.to_datetime(data['date'])

# Extract latitude and longitude from coordinate_pair column
data[['lat', 'lon']] = data['coordinate_pair'].str.extract(r'([\d\.\-]+)[NS],([\d\.\-]+)[EW]')
data['lat'] = pd.to_numeric(data['lat'], errors='coerce') * data['coordinate_pair'].str.contains('S').apply(lambda x: -1 if x else 1)
data['lon'] = pd.to_numeric(data['lon'], errors='coerce') * data['coordinate_pair'].str.contains('W').apply(lambda x: -1 if x else 1)

# Sidebar options for customization
st.sidebar.header("Map Animation Settings")
animation_speed = st.sidebar.slider("Animation Speed (Seconds)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
dot_age_off = st.sidebar.checkbox("Disable Dot Age (All Dots Equally Visible)", value=False)

# Add a play button
st.sidebar.write("Click the Play Button on the map to begin the animation.")

# Prepare data for the animation
if dot_age_off:
    # Keep all dots equally visible by not using the date column for the size
    fig = px.scatter_mapbox(data,
                            lat='lat',
                            lon='lon',
                            hover_name='nearest_location_placename',
                            hover_data=['date', 'vehicle_type', 'model', 'status', 'tags'],
                            color='vehicle_type',
                            animation_frame='date',
                            mapbox_style='carto-positron',
                            size_max=10)
else:
    # Use the date column for varying dot sizes
    data['dot_size'] = (data['date'] - data['date'].min()).dt.days + 1
    fig = px.scatter_mapbox(data,
                            lat='lat',
                            lon='lon',
                            hover_name='nearest_location_placename',
                            hover_data=['date', 'vehicle_type', 'model', 'status', 'tags'],
                            color='vehicle_type',
                            size='dot_size',
                            animation_frame='date',
                            mapbox_style='carto-positron',
                            size_max=10)

fig.update_layout(transition_duration=int(animation_speed * 1000))  # Update animation speed
fig.update_traces(marker=dict(opacity=0.6))  # Adjust marker opacity

# Render map
st.plotly_chart(fig, use_container_width=True)
with st.expander("View gpt-4o streamlit dashboard code"):
    st.code("""
# Dashboard generated for your request: "map animation geospatial analysis of vehicle losses. include a play button and add options for dot age off and animation speed"
# On data: "02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv"

import streamlit as st
import pandas as pd
import plotly.express as px

# Title for the app
st.title("Geospatial Analysis of Vehicle Losses with Map Animation")

# Load the data
file_path = 'user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv'
data = pd.read_csv(file_path, skipinitialspace=True)

# Convert date column to datetime format
data['date'] = pd.to_datetime(data['date'])

# Extract latitude and longitude from coordinate_pair column
data[['lat', 'lon']] = data['coordinate_pair'].str.extract(r'([\d\.\-]+)[NS],([\d\.\-]+)[EW]')
data['lat'] = pd.to_numeric(data['lat'], errors='coerce') * data['coordinate_pair'].str.contains('S').apply(lambda x: -1 if x else 1)
data['lon'] = pd.to_numeric(data['lon'], errors='coerce') * data['coordinate_pair'].str.contains('W').apply(lambda x: -1 if x else 1)

# Sidebar options for customization
st.sidebar.header("Map Animation Settings")
animation_speed = st.sidebar.slider("Animation Speed (Seconds)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
dot_age_off = st.sidebar.checkbox("Disable Dot Age (All Dots Equally Visible)", value=False)

# Add a play button
st.sidebar.write("Click the Play Button on the map to begin the animation.")

# Prepare data for the animation
if dot_age_off:
    # Keep all dots equally visible by not using the date column for the size
    fig = px.scatter_mapbox(data,
                            lat='lat',
                            lon='lon',
                            hover_name='nearest_location_placename',
                            hover_data=['date', 'vehicle_type', 'model', 'status', 'tags'],
                            color='vehicle_type',
                            animation_frame='date',
                            mapbox_style='carto-positron',
                            size_max=10)
else:
    # Use the date column for varying dot sizes
    data['dot_size'] = (data['date'] - data['date'].min()).dt.days + 1
    fig = px.scatter_mapbox(data,
                            lat='lat',
                            lon='lon',
                            hover_name='nearest_location_placename',
                            hover_data=['date', 'vehicle_type', 'model', 'status', 'tags'],
                            color='vehicle_type',
                            size='dot_size',
                            animation_frame='date',
                            mapbox_style='carto-positron',
                            size_max=10)

fig.update_layout(transition_duration=int(animation_speed * 1000))  # Update animation speed
fig.update_traces(marker=dict(opacity=0.6))  # Adjust marker opacity

# Render map
st.plotly_chart(fig, use_container_width=True)""", language="python")


import streamlit as st
from helpers.code_editor import code_refiner, correct_code
from config import DASHBOARD_REFINER_SUGGESTIONS, BOT_RESPONSE_REFINED
from random import randint

# Load SVG assets
with open("data/resources/doggie.svg", "r") as bot_file:
    bot_svg = bot_file.read()

# Ensure session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

def add_message(input_message):
    """Handles input from the chat input component."""
    if input_message.strip():

        # Existing code for the dashboard
        existing_code = """import streamlit as st
import pandas as pd
import plotly.express as px

# Title for the app
st.title("Geospatial Analysis of Vehicle Losses with Map Animation")

# Load the data
file_path = 'user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv'
data = pd.read_csv(file_path, skipinitialspace=True)

# Convert date column to datetime format
data['date'] = pd.to_datetime(data['date'])

# Extract latitude and longitude from coordinate_pair column
data[['lat', 'lon']] = data['coordinate_pair'].str.extract(r'([\d\.\-]+)[NS],([\d\.\-]+)[EW]')
data['lat'] = pd.to_numeric(data['lat'], errors='coerce') * data['coordinate_pair'].str.contains('S').apply(lambda x: -1 if x else 1)
data['lon'] = pd.to_numeric(data['lon'], errors='coerce') * data['coordinate_pair'].str.contains('W').apply(lambda x: -1 if x else 1)

# Sidebar options for customization
st.sidebar.header("Map Animation Settings")
animation_speed = st.sidebar.slider("Animation Speed (Seconds)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
dot_age_off = st.sidebar.checkbox("Disable Dot Age (All Dots Equally Visible)", value=False)

# Add a play button
st.sidebar.write("Click the Play Button on the map to begin the animation.")

# Prepare data for the animation
if dot_age_off:
    # Keep all dots equally visible by not using the date column for the size
    fig = px.scatter_mapbox(data,
                            lat='lat',
                            lon='lon',
                            hover_name='nearest_location_placename',
                            hover_data=['date', 'vehicle_type', 'model', 'status', 'tags'],
                            color='vehicle_type',
                            animation_frame='date',
                            mapbox_style='carto-positron',
                            size_max=10)
else:
    # Use the date column for varying dot sizes
    data['dot_size'] = (data['date'] - data['date'].min()).dt.days + 1
    fig = px.scatter_mapbox(data,
                            lat='lat',
                            lon='lon',
                            hover_name='nearest_location_placename',
                            hover_data=['date', 'vehicle_type', 'model', 'status', 'tags'],
                            color='vehicle_type',
                            size='dot_size',
                            animation_frame='date',
                            mapbox_style='carto-positron',
                            size_max=10)

fig.update_layout(transition_duration=int(animation_speed * 1000))  # Update animation speed
fig.update_traces(marker=dict(opacity=0.6))  # Adjust marker opacity

# Render map
st.plotly_chart(fig, use_container_width=True)"""

        # Refine code based on input
        new_code = code_refiner(existing_code, input_message)

        user_requests = f"""# Dashboard generated for your request: "{input_message}"
"""

        # Optionally execute the new code (be cautious of dynamic exec)
        try:
            exec(new_code, {})
        except Exception as e:
            print("ERROR:", e)
            correct_code(new_code, e)
            st.toast("Too many errors, try a different dashboard modification")

        # Display assistant response
        assistant_message = st.chat_message("assistant", avatar=bot_svg)
        assistant_message.write(BOT_RESPONSE_REFINED[randint(0, len(BOT_RESPONSE_REFINED)-1)])
        assistant_message.expander("View llama3-70b-8192 refined dashboard code").code(f"""{user_requests}{new_code}""", language="python")

# Add the chat input field
input_message = st.chat_input(placeholder="Use a scatter plot to visualize correlations")


if input_message:
    st.chat_message("user", avatar=":material/person:").write(input_message)
    add_message(input_message)
    