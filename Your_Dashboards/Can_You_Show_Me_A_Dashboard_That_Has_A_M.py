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

import streamlit as st
from streamlit.components.v1 import html
from helpers.code_editor import code_refiner, correct_code
from streamlit_extras.sandbox import sandbox


def render_svg(svg_string):
    """Renders the given svg string."""
    c = st.container()
    with c:
        html(svg_string)

# Assuming the PNG is in the 'images' directory
user_svg = open("data/resources/doggie.svg", "r").read()
bot_svg = open("data/resources/user.svg", "r").read()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages with custom SVGs
def display_messages():
    for msg in st.session_state.messages:
        if msg["is_user"]:
            # User message with custom SVG
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-end; align-items: center; margin: 10px 0;">
                    <div style="max-width: 70%; padding: 10px; border-radius: 10px;">
                        {msg["content"]}
                    </div>
                    {bot_svg}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Bot message with custom SVG
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-start; align-items: center; margin: 10px 0;">
                    {user_svg}
                    <div style="max-width: 70%; padding: 10px; border-radius: 10px;">
                        {msg["content"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# Add the chat input area
new_dash_message = 'Check the top of the page for your new dashboard.'
def add_message():
    if st.session_state.input_message.strip():
        # Add user message
        st.session_state.messages.append({"content": st.session_state.input_message, "is_user": True})
        # refine already existing code
        new_code = code_refiner("""import streamlit as st
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
st.dataframe(df_grouped)""", st.session_state.input_message)
        exec(new_code, {})
        st.session_state.messages.append({"content": new_dash_message, "is_user": False})
        st.session_state.input_message = ""


# Style the input box to stick at the bottom
st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] {
        position: fixed;
        bottom: 0;
        width: 100%;
        z-index: 100;
        background-color: #ffffff;
        padding: 10px 20px;
        box-shadow: 0px -2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display chat messages
display_messages()

# Create the input bar
with st.container():
    st.subheader("Dashboard Editor")
    st.text_input("Dashboard editor",
                key="input_message",
                on_change=add_message,
                placeholder="I want a pie chart instead of a bar chart",
                label_visibility="collapsed"
    )

st.subheader('')


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
