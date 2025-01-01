import streamlit as st
st.set_page_config(page_icon="🤖", layout="centered")
from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv')

# Convert the date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Extract the month and year from the date column
df['month'] = df['date'].dt.strftime('%Y-%m')

# Group the data by month and count the losses
monthly_losses = df.groupby('month').size().reset_index(name='losses')

# Create a pie chart
st.title("Monthly Losses")
fig, ax = plt.subplots(figsize=(10, 8))
ax.pie(monthly_losses['losses'], labels=monthly_losses['month'], autopct='%1.1f%%')
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)

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
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv')

# Convert the date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Extract the month and year from the date column
df['month'] = df['date'].dt.strftime('%Y-%m')

# Group the data by month and count the losses
monthly_losses = df.groupby('month').size().reset_index(name='losses')

# Create a pie chart
st.title("Monthly Losses")
fig, ax = plt.subplots(figsize=(10, 8))
ax.pie(monthly_losses['losses'], labels=monthly_losses['month'], autopct='%1.1f%%')
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)""", st.session_state.input_message)
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

    

st.markdown("""Dashboard generated for your request: \"pie chart monthly losses\" """)
st.markdown("""On data: \"02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv\" """)

        
st.markdown("""llama3-70b-8192 generated code:""")
st.code("""import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv')

# Convert the date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Extract the month and year from the date column
df['month'] = df['date'].dt.strftime('%Y-%m')

# Group the data by month and count the losses
monthly_losses = df.groupby('month').size().reset_index(name='losses')

# Create a pie chart
st.title("Monthly Losses")
fig, ax = plt.subplots(figsize=(10, 8))
ax.pie(monthly_losses['losses'], labels=monthly_losses['month'], autopct='%1.1f%%')
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)""", language="python")
