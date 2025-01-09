import streamlit as st
st.set_page_config(page_icon="🤖", layout="centered")
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import streamlit as st
import pandas as pd

# Set the title of the Streamlit app
st.title("Map of Vehicle Losses")

# Load the data
file_path = 'user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv'
data = pd.read_csv(file_path)

# Data preprocessing
# Extract latitude and longitude from the 'lat' and 'lon' columns
data['latitude'] = data['lat'].str.extract(r'([0-9.]+)').astype(float)
data['longitude'] = data['lon'].str.extract(r'([0-9.]+)').astype(float)

# Filter out rows with missing or invalid coordinates
map_data = data.dropna(subset=['latitude', 'longitude'])

# Display the map
st.map(map_data[['latitude', 'longitude']])
with st.expander("View gpt-4o streamlit dashboard code"):
    st.code("""
# Dashboard generated for your request: "map of losses"
# On data: "02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv"

import streamlit as st
import pandas as pd

# Set the title of the Streamlit app
st.title("Map of Vehicle Losses")

# Load the data
file_path = 'user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv'
data = pd.read_csv(file_path)

# Data preprocessing
# Extract latitude and longitude from the 'lat' and 'lon' columns
data['latitude'] = data['lat'].str.extract(r'([0-9.]+)').astype(float)
data['longitude'] = data['lon'].str.extract(r'([0-9.]+)').astype(float)

# Filter out rows with missing or invalid coordinates
map_data = data.dropna(subset=['latitude', 'longitude'])

# Display the map
st.map(map_data[['latitude', 'longitude']])""", language="python")

st.caption(f"Dashboard created at 2025-01-09 10:17:21")



import streamlit as st
from helpers.code_editor import code_refiner, correct_code
from config import BOT_RESPONSE_REFINED, CODE_REFINER_MODEL
from random import randint
import os
from message_utils import get_file_messages, add_user_message, add_assistant_message

FILENAME = os.path.basename(__file__)


# Load SVG assets
with open("data/resources/doggie.svg", "r") as bot_file:
    bot_svg = bot_file.read()
with open("data/resources/person.svg", "r") as person_file:
    person_svg = person_file.read()

st.session_state.messages = []
st.session_state.messages = get_file_messages(FILENAME)

# Ensure session state for messages
    # Load messages for the user from persistent storage

# Display existing messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        old_user_message = st.chat_message("user", avatar=person_svg)
        old_user_message.write(msg["message_contents"])
    elif msg["role"] == "assistant":
        try:
            exec(msg["assistant_code"], {})
        # except Exception as e:
        #     exec(correct_code(msg["assistant_code"], e), {})
        except Exception as e:
            print(e)
            st.toast("Too many errors, try a different dashboard modification")
            errored = True

        old_a_message = st.chat_message("assistant", avatar=bot_svg)
        old_a_message.write(msg["message_contents"])
        old_a_message.expander(msg["assistant_code_expander"]).code(msg["assistant_code_top"]+msg["assistant_code"], language="python")
        # old_a_message.caption(msg["timestamp"])


def add_message(input_message, user_email):
    """Handles input from the chat input component."""
    if input_message.strip():

        # Existing code for the dashboard
        existing_code = """import streamlit as st
import pandas as pd

# Set the title of the Streamlit app
st.title("Map of Vehicle Losses")

# Load the data
file_path = 'user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv'
data = pd.read_csv(file_path)

# Data preprocessing
# Extract latitude and longitude from the 'lat' and 'lon' columns
data['latitude'] = data['lat'].str.extract(r'([0-9.]+)').astype(float)
data['longitude'] = data['lon'].str.extract(r'([0-9.]+)').astype(float)

# Filter out rows with missing or invalid coordinates
map_data = data.dropna(subset=['latitude', 'longitude'])

# Display the map
st.map(map_data[['latitude', 'longitude']])"""

        # Refine code based on input

        new_code = correct_code(code_refiner(existing_code, f"""{input_message}
Snippet(s) of the user's files: 'user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv': "Columns and Data Types:
  - id: int64
  - lat: string
  - lon: string
  - coordinate_pair: string
  - nearest_location_placename: string
  - date: date
  - vehicle_type: categorical
  - model: string
  - unit: string
  - status: categorical
  - tags: string

Preview of Rows:
  id                 lat                 lon                         coordinate_pair          nearest_location_placename       date               vehicle_type                 model                                 unit    status          tags
 602 50.055203497014496N 36.361463815056865E 50.055203497014496N,36.361463815056865E              Kharkiv, Kharkiv raion 2022-02-24                      Tanks               T-80BVM   200th Separate Motor Rifle Brigade Destroyed    Turretless
 954          50.054933N          36.360974E                   50.054933N,36.360974E              Kharkiv, Kharkiv raion 2022-02-24 Infantry fighting vehicles            MT-LBVM(K)    25th Separate Motor Rifle Brigade Destroyed           NaN
1367            51.6151N           31.22244E                      51.6151N,31.22244E        Rivnopillia, Chernihiv raion 2022-02-24 Infantry fighting vehicles              BMP-2(K)    74th Separate Motor Rifle Brigade Destroyed Turretless, O
1590                 NaN                 NaN                               None,None Stanytsia Luhanska, Shchastia raion 2022-02-24 Infantry fighting vehicles              BMP-2(K)                                  NaN  Captured             Z
2251          50.312451N          34.864655E                   50.312451N,34.864655E            Okhtyrka, Okhtyrka raion 2022-02-24 Infantry mobility vehicles KamAZ-63968 'Typhoon' 96th Separate Reconnaissance Brigade  Captured           NaN"
These are the file path(s): ['user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv']"""), 'fix any potential errors')
        user_requests = f"""# Dashboard generated for your request: "{input_message}"
"""
        
        # Display assistant response
        assistant_message = st.chat_message("assistant", avatar=bot_svg)
        bot_response = BOT_RESPONSE_REFINED[randint(0, len(BOT_RESPONSE_REFINED)-1)]
        code_expander_text = f"View {CODE_REFINER_MODEL} refined dashboard code"
        code_in_expander = f"""{user_requests}{new_code}"""
        assistant_message.write(bot_response)
        assistant_message.expander(code_expander_text).code(code_in_expander, language="python")

        # Add the user message to messages.json
        add_user_message(file_path=FILENAME, message_contents=input_message, user_id=user_email)
        # Add the assistant message to messages.json
        add_assistant_message(file_path=FILENAME,
                              message_contents=bot_response,
                              assistant_code_expander=code_expander_text,
                              assistant_code=new_code,
                              assistant_code_top=user_requests,
        )

# Add the chat input field
input_message = st.chat_input(placeholder=f"Include a comparison against last year's data")

if 'user_info' in st.session_state and st.session_state.user_info and st.session_state.user_info['email']:
    user_email = st.session_state.user_info['email']
else:
    user_email = 'no_email'

if input_message:
    st.chat_message("user", avatar=person_svg).write(input_message)
    add_message(input_message, user_email)
    