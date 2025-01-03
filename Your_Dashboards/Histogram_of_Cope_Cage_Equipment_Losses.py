import streamlit as st
st.set_page_config(page_icon="🤖", layout="centered")
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

st.title("Histogram of Cope Cage Equipment Losses")

# Load the data from the JSON file
with open('user_uploaded_files/russia_losses.json', 'r') as f:
    data = json.load(f)

# Create a DataFrame from the data
df = pd.DataFrame(data['losses'])

# Filter the DataFrame to only include equipment with 'Cope cage' in the tags
cope_cage_df = df[df['tags'].str.contains('Cope cage', na=False)]

# Create a histogram of the equipment types
fig, ax = plt.subplots()
ax.bar(cope_cage_df['type'].value_counts().index, cope_cage_df['type'].value_counts().values)
ax.set_xlabel('Equipment Type')
ax.set_ylabel('Count')
ax.set_title('Histogram of Cope Cage Equipment Losses')
st.pyplot(fig)
with st.expander("View llama-3.3-70b-specdec streamlit dashboard code"):
    st.code("""
# Dashboard generated for your request: "histogram of only cope cage"
# On data: "russia_losses.json"

import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

st.title("Histogram of Cope Cage Equipment Losses")

# Load the data from the JSON file
with open('user_uploaded_files/russia_losses.json', 'r') as f:
    data = json.load(f)

# Create a DataFrame from the data
df = pd.DataFrame(data['losses'])

# Filter the DataFrame to only include equipment with 'Cope cage' in the tags
cope_cage_df = df[df['tags'].str.contains('Cope cage', na=False)]

# Create a histogram of the equipment types
fig, ax = plt.subplots()
ax.bar(cope_cage_df['type'].value_counts().index, cope_cage_df['type'].value_counts().values)
ax.set_xlabel('Equipment Type')
ax.set_ylabel('Count')
ax.set_title('Histogram of Cope Cage Equipment Losses')
st.pyplot(fig)""", language="python")


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
import json
import pandas as pd
import matplotlib.pyplot as plt

st.title("Histogram of Cope Cage Equipment Losses")

# Load the data from the JSON file
with open('user_uploaded_files/russia_losses.json', 'r') as f:
    data = json.load(f)

# Create a DataFrame from the data
df = pd.DataFrame(data['losses'])

# Filter the DataFrame to only include equipment with 'Cope cage' in the tags
cope_cage_df = df[df['tags'].str.contains('Cope cage', na=False)]

# Create a histogram of the equipment types
fig, ax = plt.subplots()
ax.bar(cope_cage_df['type'].value_counts().index, cope_cage_df['type'].value_counts().values)
ax.set_xlabel('Equipment Type')
ax.set_ylabel('Count')
ax.set_title('Histogram of Cope Cage Equipment Losses')
st.pyplot(fig)"""

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
            st.toast("Too many errors :skull_and_crossbones:")

        # Display assistant response
        assistant_message = st.chat_message("assistant", avatar=bot_svg)
        assistant_message.write(BOT_RESPONSE_REFINED[randint(0, len(BOT_RESPONSE_REFINED)-1)])
        assistant_message.expander("View llama3-70b-8192 refined dashboard code").code(f"""{user_requests}{new_code}""", language="python")

# Add the chat input field
input_message = st.chat_input(placeholder="Add percentage labels to the pie chart")


if input_message:
    st.chat_message("user", avatar=":material/person:").write(input_message)
    add_message(input_message)
    