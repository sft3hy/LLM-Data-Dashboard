import streamlit as st
st.set_page_config(page_icon="🤖", layout="centered")
from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import json
import altair as alt

# Load the JSON file
file_path = 'user_uploaded_files/russia_losses.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Convert the JSON data to a pandas DataFrame
df = pd.json_normalize(data['losses'])

# Create the Streamlit app
st.title("Russia Losses Visualization")

# Bar Chart 1: Count of Equipment Types
equipment_type_count = df['type'].value_counts().reset_index()
equipment_type_count.columns = ['Type', 'Count']

st.subheader("Count of Equipment Types")
chart_1 = alt.Chart(equipment_type_count).mark_bar().encode(
    x=alt.X('Type', sort='-y', title='Equipment Type'),
    y=alt.Y('Count', title='Count'),
    tooltip=['Type', 'Count']
).properties(
    width=700,
    height=400
)
st.altair_chart(chart_1)

# Bar Chart 2: Status Count
status_count = df['status'].value_counts().reset_index()
status_count.columns = ['Status', 'Count']

st.subheader("Count of Equipment by Status")
chart_2 = alt.Chart(status_count).mark_bar().encode(
    x=alt.X('Status', sort='-y', title='Status'),
    y=alt.Y('Count', title='Count'),
    tooltip=['Status', 'Count']
).properties(
    width=700,
    height=400
)
st.altair_chart(chart_2)

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
import json
import altair as alt

# Load the JSON file
file_path = 'user_uploaded_files/russia_losses.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Convert the JSON data to a pandas DataFrame
df = pd.json_normalize(data['losses'])

# Create the Streamlit app
st.title("Russia Losses Visualization")

# Bar Chart 1: Count of Equipment Types
equipment_type_count = df['type'].value_counts().reset_index()
equipment_type_count.columns = ['Type', 'Count']

st.subheader("Count of Equipment Types")
chart_1 = alt.Chart(equipment_type_count).mark_bar().encode(
    x=alt.X('Type', sort='-y', title='Equipment Type'),
    y=alt.Y('Count', title='Count'),
    tooltip=['Type', 'Count']
).properties(
    width=700,
    height=400
)
st.altair_chart(chart_1)

# Bar Chart 2: Status Count
status_count = df['status'].value_counts().reset_index()
status_count.columns = ['Status', 'Count']

st.subheader("Count of Equipment by Status")
chart_2 = alt.Chart(status_count).mark_bar().encode(
    x=alt.X('Status', sort='-y', title='Status'),
    y=alt.Y('Count', title='Count'),
    tooltip=['Status', 'Count']
).properties(
    width=700,
    height=400
)
st.altair_chart(chart_2)""", st.session_state.input_message)
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
    st.text_input("Dashboard editor",
                key="input_message",
                on_change=add_message,
                placeholder="I want a pie chart instead of a bar chart")

    

st.markdown("""Dashboard generated for your request: \"bar charts, 2\" """)
st.markdown("""On data: \"russia_losses.json\" """)

        
st.markdown("""gpt-4o generated code:""")
st.code("""import streamlit as st
import pandas as pd
import json
import altair as alt

# Load the JSON file
file_path = 'user_uploaded_files/russia_losses.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Convert the JSON data to a pandas DataFrame
df = pd.json_normalize(data['losses'])

# Create the Streamlit app
st.title("Russia Losses Visualization")

# Bar Chart 1: Count of Equipment Types
equipment_type_count = df['type'].value_counts().reset_index()
equipment_type_count.columns = ['Type', 'Count']

st.subheader("Count of Equipment Types")
chart_1 = alt.Chart(equipment_type_count).mark_bar().encode(
    x=alt.X('Type', sort='-y', title='Equipment Type'),
    y=alt.Y('Count', title='Count'),
    tooltip=['Type', 'Count']
).properties(
    width=700,
    height=400
)
st.altair_chart(chart_1)

# Bar Chart 2: Status Count
status_count = df['status'].value_counts().reset_index()
status_count.columns = ['Status', 'Count']

st.subheader("Count of Equipment by Status")
chart_2 = alt.Chart(status_count).mark_bar().encode(
    x=alt.X('Status', sort='-y', title='Status'),
    y=alt.Y('Count', title='Count'),
    tooltip=['Status', 'Count']
).properties(
    width=700,
    height=400
)
st.altair_chart(chart_2)""", language="python")
