import streamlit as st
st.set_page_config(page_icon="🤖", layout="centered")
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Title of the dashboard
st.title("Weekly Vehicle Losses Analysis")

# Load the data
file_path = 'user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv'
data = pd.read_csv(file_path)

# Parse the 'date' column to datetime
data['date'] = pd.to_datetime(data['date'], errors='coerce')

# Filter rows with valid dates
data = data.dropna(subset=['date'])

# Calculate the week number and year for weekly aggregation
data['year_week'] = data['date'].dt.strftime('%Y-W%U')

# Aggregate vehicle losses by week
weekly_losses = data.groupby('year_week').size().reset_index(name='vehicle_losses')

# Sort by week
weekly_losses = weekly_losses.sort_values('year_week')

# Visualization
st.bar_chart(
    data=weekly_losses.set_index('year_week')['vehicle_losses'],
    use_container_width=True,
    height=400
)

# Additional notes
st.write("This bar chart displays weekly vehicle losses based on the provided dataset.")
st.write("Make sure date data is correctly formatted to ensure accurate calculations.")
with st.expander("View gpt-4o streamlit dashboard code"):
    st.code("""
# Dashboard generated for your request: "bar chart weekly losses"
# On data: "02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv"

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Title of the dashboard
st.title("Weekly Vehicle Losses Analysis")

# Load the data
file_path = 'user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv'
data = pd.read_csv(file_path)

# Parse the 'date' column to datetime
data['date'] = pd.to_datetime(data['date'], errors='coerce')

# Filter rows with valid dates
data = data.dropna(subset=['date'])

# Calculate the week number and year for weekly aggregation
data['year_week'] = data['date'].dt.strftime('%Y-W%U')

# Aggregate vehicle losses by week
weekly_losses = data.groupby('year_week').size().reset_index(name='vehicle_losses')

# Sort by week
weekly_losses = weekly_losses.sort_values('year_week')

# Visualization
st.bar_chart(
    data=weekly_losses.set_index('year_week')['vehicle_losses'],
    use_container_width=True,
    height=400
)

# Additional notes
st.write("This bar chart displays weekly vehicle losses based on the provided dataset.")
st.write("Make sure date data is correctly formatted to ensure accurate calculations.")""", language="python")


import streamlit as st
from helpers.code_editor import code_refiner, correct_code
from config import BOT_RESPONSE_REFINED, CODE_REFINER_MODEL
from random import randint
import os
from message_utils import get_file_messages, add_user_message, add_assistant_message
from config import GENERATED_FILES_DIR

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
        except Exception as e:
            print(e)
            st.toast("Too many errors, try a different dashboard modification")
            errored = True

        old_a_message = st.chat_message("assistant", avatar=bot_svg)
        old_a_message.write(msg["message_contents"])
        old_a_message.expander(msg["assistant_code_expander"]).code(msg["assistant_code_top"]+msg["assistant_code"], language="python")
        # old_a_message.caption(msg["timestamp"])


def add_message(input_message):
    """Handles input from the chat input component."""
    if input_message.strip():

        # Existing code for the dashboard
        existing_code = """import streamlit as st
import pandas as pd

# Load the data
file_path = "user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv"
data = pd.read_csv(file_path)

# Prepare the data for the bar chart
data_counts = data['status'].value_counts()

# Display the bar chart
st.title("Vehicle Losses Bar Chart")
st.bar_chart(data_counts)"""

        # Refine code based on input

        new_code = correct_code(code_refiner(existing_code, f"""{input_message}
Snippet(s) of the user's files: 'user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv': "Columns and Data Types:\n  - id: int64\n  - lat: string\n  - lon: string\n  - coordinate_pair: string\n  - nearest_location_placename: string\n  - date: date\n  - vehicle_type: categorical\n  - model: string\n  - unit: string\n  - status: categorical\n  - tags: string\n\nPreview of Rows:\n  id                 lat                 lon                         coordinate_pair          nearest_location_placename       date               vehicle_type                 model                                 unit    status          tags\n 602 50.055203497014496N 36.361463815056865E 50.055203497014496N,36.361463815056865E              Kharkiv, Kharkiv raion 2022-02-24                      Tanks               T-80BVM   200th Separate Motor Rifle Brigade Destroyed    Turretless\n 954          50.054933N          36.360974E                   50.054933N,36.360974E              Kharkiv, Kharkiv raion 2022-02-24 Infantry fighting vehicles            MT-LBVM(K)    25th Separate Motor Rifle Brigade Destroyed           NaN\n1367            51.6151N           31.22244E                      51.6151N,31.22244E        Rivnopillia, Chernihiv raion 2022-02-24 Infantry fighting vehicles              BMP-2(K)    74th Separate Motor Rifle Brigade Destroyed Turretless, O\n1590                 NaN                 NaN                               None,None Stanytsia Luhanska, Shchastia raion 2022-02-24 Infantry fighting vehicles              BMP-2(K)                                  NaN  Captured             Z\n2251          50.312451N          34.864655E                   50.312451N,34.864655E            Okhtyrka, Okhtyrka raion 2022-02-24 Infantry mobility vehicles KamAZ-63968 'Typhoon' 96th Separate Reconnaissance Brigade  Captured           NaN"
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
        add_user_message(file_path=FILENAME, message_contents=input_message)
        # Add the assistant message to messages.json
        add_assistant_message(file_path=FILENAME,
                              message_contents=bot_response,
                              assistant_code_expander=code_expander_text,
                              assistant_code=new_code,
                              assistant_code_top=user_requests,
        )

# Add the chat input field
input_message = st.chat_input(placeholder=f"Show the data as a histogram instead of a line chart")


if input_message:
    st.chat_message("user", avatar=person_svg).write(input_message)
    add_message(input_message)
    