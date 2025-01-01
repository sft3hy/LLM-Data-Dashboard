from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import json
import pydeck as pdk

st.set_page_config(page_title="Cope Cage Map", page_icon=":robot_face:", layout="centered")


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
                        {{msg["content"]}}
                    </div>
                    {{bot_svg}}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Bot message with custom SVG
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-start; align-items: center; margin: 10px 0;">
                    {{user_svg}}
                    <div style="max-width: 70%; padding: 10px; border-radius: 10px;">
                        {{msg["content"]}}
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
        st.session_state.messages.append({{"content": st.session_state.input_message, "is_user": True}})
        # refine already existing code
        new_code = code_refiner("""from streamlit_folium import folium_static
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
    st.write("No data with 'Cope cage' and geo coordinates available.")""", st.session_state.input_message)
        exec(new_code, {})
        st.session_state.messages.append({{"content": new_dash_message, "is_user": False}})
        st.session_state.input_message = ""


# Style the input box to stick at the bottom
st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] {{
        position: fixed;
        bottom: 0;
        width: 100%;
        z-index: 100;
        background-color: #ffffff;
        padding: 10px 20px;
        box-shadow: 0px -2px 5px rgba(0,0,0,0.1);
    }}
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
st.markdown("""Dashboard generated for your request: \"Cope cage map\" """)
st.markdown("""On data: \"russia_losses.json\"""")

        
st.markdown("""gpt-4o generated code:""")
st.code("""from streamlit_folium import folium_static
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
    st.write("No data with 'Cope cage' and geo coordinates available.")""",
    language="python")