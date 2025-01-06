import streamlit as st
st.set_page_config(page_icon="🤖", layout="centered")
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import streamlit as st
import pandas as pd
import datetime as dt

# Title
st.title("Analysis of Fatalities in the Israeli-Palestinian Conflict (2000-2023)")

# Load data
file_path = 'user_uploaded_files/fatalities_isr_pse_conflict_2000_to_2023.csv'
data = pd.read_csv(file_path, parse_dates=['date_of_event', 'date_of_death'])

# Cleanup and processing
data['year_of_event'] = data['date_of_event'].dt.year

# Graph 1: Fatalities Over Time (Year)
st.subheader("Fatalities Over Time (Years)")
fatalities_by_year = data.groupby('year_of_event').size().reset_index(name='count')
st.line_chart(fatalities_by_year.set_index('year_of_event'))

# Graph 2: Fatalities by Event Location Region
st.subheader("Fatalities by Event Location Region")
fatalities_by_region = data['event_location_region'].value_counts()
st.bar_chart(fatalities_by_region)

# Graph 3: Age Distribution of Fatalities
st.subheader("Age Distribution of Fatalities")
st.bar_chart(data['age'].value_counts().sort_index())

# Graph 4: Gender Distribution of Fatalities
st.subheader("Gender Distribution of Fatalities")
gender_distribution = data['gender'].value_counts()
st.bar_chart(gender_distribution)

# Graph 5: Map of Fatality Locations
st.subheader("Map of Fatalities")
# Generate dummy coordinates to simulate map data (in a real scenario, proper lat/lon data is needed)
data['latitude'] = data.index / len(data) * 2 + 31  # Simulating latitudes between 31 and 33
data['longitude'] = data.index / len(data) * 2 + 34  # Simulating longitudes between 34 and 36
st.map(data[['latitude', 'longitude']])

# Graph 6: Fatalities by Ammunition Type
st.subheader("Fatalities by Ammunition Type")
fatalities_by_ammunition = data['ammunition'].value_counts()
st.bar_chart(fatalities_by_ammunition)

st.write("Data source: Israeli-Palestinian Conflict Dataset (2000-2023)")
with st.expander("View gpt-4o streamlit dashboard code"):
    st.code("""
# Dashboard generated for your request: "several informative graphs"
# On data: "fatalities_isr_pse_conflict_2000_to_2023.csv"

import streamlit as st
import pandas as pd
import datetime as dt

# Title
st.title("Analysis of Fatalities in the Israeli-Palestinian Conflict (2000-2023)")

# Load data
file_path = 'user_uploaded_files/fatalities_isr_pse_conflict_2000_to_2023.csv'
data = pd.read_csv(file_path, parse_dates=['date_of_event', 'date_of_death'])

# Cleanup and processing
data['year_of_event'] = data['date_of_event'].dt.year

# Graph 1: Fatalities Over Time (Year)
st.subheader("Fatalities Over Time (Years)")
fatalities_by_year = data.groupby('year_of_event').size().reset_index(name='count')
st.line_chart(fatalities_by_year.set_index('year_of_event'))

# Graph 2: Fatalities by Event Location Region
st.subheader("Fatalities by Event Location Region")
fatalities_by_region = data['event_location_region'].value_counts()
st.bar_chart(fatalities_by_region)

# Graph 3: Age Distribution of Fatalities
st.subheader("Age Distribution of Fatalities")
st.bar_chart(data['age'].value_counts().sort_index())

# Graph 4: Gender Distribution of Fatalities
st.subheader("Gender Distribution of Fatalities")
gender_distribution = data['gender'].value_counts()
st.bar_chart(gender_distribution)

# Graph 5: Map of Fatality Locations
st.subheader("Map of Fatalities")
# Generate dummy coordinates to simulate map data (in a real scenario, proper lat/lon data is needed)
data['latitude'] = data.index / len(data) * 2 + 31  # Simulating latitudes between 31 and 33
data['longitude'] = data.index / len(data) * 2 + 34  # Simulating longitudes between 34 and 36
st.map(data[['latitude', 'longitude']])

# Graph 6: Fatalities by Ammunition Type
st.subheader("Fatalities by Ammunition Type")
fatalities_by_ammunition = data['ammunition'].value_counts()
st.bar_chart(fatalities_by_ammunition)

st.write("Data source: Israeli-Palestinian Conflict Dataset (2000-2023)")""", language="python")


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


def add_message(input_message):
    """Handles input from the chat input component."""
    if input_message.strip():

        # Existing code for the dashboard
        existing_code = """import streamlit as st
import pandas as pd
import datetime as dt

# Title
st.title("Analysis of Fatalities in the Israeli-Palestinian Conflict (2000-2023)")

# Load data
file_path = 'user_uploaded_files/fatalities_isr_pse_conflict_2000_to_2023.csv'
data = pd.read_csv(file_path, parse_dates=['date_of_event', 'date_of_death'])

# Cleanup and processing
data['year_of_event'] = data['date_of_event'].dt.year

# Graph 1: Fatalities Over Time (Year)
st.subheader("Fatalities Over Time (Years)")
fatalities_by_year = data.groupby('year_of_event').size().reset_index(name='count')
st.line_chart(fatalities_by_year.set_index('year_of_event'))

# Graph 2: Fatalities by Event Location Region
st.subheader("Fatalities by Event Location Region")
fatalities_by_region = data['event_location_region'].value_counts()
st.bar_chart(fatalities_by_region)

# Graph 3: Age Distribution of Fatalities
st.subheader("Age Distribution of Fatalities")
st.bar_chart(data['age'].value_counts().sort_index())

# Graph 4: Gender Distribution of Fatalities
st.subheader("Gender Distribution of Fatalities")
gender_distribution = data['gender'].value_counts()
st.bar_chart(gender_distribution)

# Graph 5: Map of Fatality Locations
st.subheader("Map of Fatalities")
# Generate dummy coordinates to simulate map data (in a real scenario, proper lat/lon data is needed)
data['latitude'] = data.index / len(data) * 2 + 31  # Simulating latitudes between 31 and 33
data['longitude'] = data.index / len(data) * 2 + 34  # Simulating longitudes between 34 and 36
st.map(data[['latitude', 'longitude']])

# Graph 6: Fatalities by Ammunition Type
st.subheader("Fatalities by Ammunition Type")
fatalities_by_ammunition = data['ammunition'].value_counts()
st.bar_chart(fatalities_by_ammunition)

st.write("Data source: Israeli-Palestinian Conflict Dataset (2000-2023)")"""

        # Refine code based on input

        new_code = correct_code(code_refiner(existing_code, f"""{input_message}
Snippet(s) of the user's files: 'user_uploaded_files/fatalities_isr_pse_conflict_2000_to_2023.csv': "Columns and Data Types:\n  - name: string\n  - date_of_event: date\n  - age: float64\n  - citizenship: categorical\n  - event_location: string\n  - event_location_district: string\n  - event_location_region: categorical\n  - date_of_death: date\n  - gender: categorical\n  - took_part_in_the_hostilities: categorical\n  - place_of_residence: string\n  - place_of_residence_district: string\n  - type_of_injury: string\n  - ammunition: string\n  - killed_by: categorical\n  - notes: string\n\nPreview of Rows:\n                                       name date_of_event  age citizenship    event_location event_location_district event_location_region date_of_death gender took_part_in_the_hostilities place_of_residence place_of_residence_district type_of_injury      ammunition               killed_by                                                                                                                                                                                                                                                                                                                                                                                                     notes\n'Abd a-Rahman Suleiman Muhammad Abu Daghash    2023-09-24 32.0 Palestinian    Nur Shams R.C.                 Tulkarm             West Bank    2023-09-24      M                          NaN     Nur Shams R.C.                     Tulkarm        gunfire live ammunition Israeli security forces                                                  Fatally shot by Israeli forces while standing on the roof of his home, watching clashes that erupted between them and young men after the forces entered the camp. During the forces’ incursion into the camp, another Palestinian was killed while fleeing the forces. According to the IDF Spokesperson, a soldier was moderately injured by shrapnel.\n       Usayed Farhan Muhammad 'Ali Abu 'Ali    2023-09-24 21.0 Palestinian    Nur Shams R.C.                 Tulkarm             West Bank    2023-09-24      M                          NaN     Nur Shams R.C.                     Tulkarm        gunfire live ammunition Israeli security forces Fatally shot by Israeli forces while trying to flee them after watching clashes that erupted after they entered the camp and included a fire exchange. Abu ‘Ali was a Hamas military wing operative. During the forces’ incursion into the camp, another Palestinian was killed while standing on the roof of his house. According to the IDF Spokesperson, a soldier was moderately injured by shrapnel.\n           'Abdallah 'Imad Sa'ed Abu Hassan    2023-09-22 16.0 Palestinian          Kfar Dan                   Jenin             West Bank    2023-09-22      M                          NaN           al-Yamun                       Jenin        gunfire live ammunition Israeli security forces                                                                                                                                                                                                         Fatally shot by soldiers while firing at them with an improvised gun during a fire exchange that erupted after they entered the village. Abu Hassan was an Islamic Jihad military wing operative.\n           Durgham Muhammad Yihya al-Akhras    2023-09-20 19.0 Palestinian 'Aqbat Jaber R.C.                 Jericho             West Bank    2023-09-20      M                          NaN  'Aqbat Jaber R.C.                     Jericho        gunfire live ammunition Israeli security forces                                                                                                                                                                                                                        Shot in the head by Israeli forces while throwing stones at them in clashes that erupted after they entered the camp and during which explosive devices were thrown at the forces.\n               Raafat 'Omar Ahmad Khamaisah    2023-09-19 15.0 Palestinian        Jenin R.C.                   Jenin             West Bank    2023-09-19      M                          NaN              Jenin                       Jenin        gunfire live ammunition Israeli security forces                        Wounded by soldiers’ gunfire after running away from them as they entered the camp. Soldiers also fired at a man who tried to evacuate him but did not hit him. Khamaiseh subsequently died of his wounds. Two Islamic Jihad military wing operatives were also killed in the incident. Another operative was wounded by the shrapnel and died of his wounds on 20 September 2023."
These are the file path(s): ['user_uploaded_files/fatalities_isr_pse_conflict_2000_to_2023.csv']"""), 'fix any potential errors')
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
input_message = st.chat_input(placeholder=f"Show cumulative totals instead of daily changes")


if input_message:
    st.chat_message("user", avatar=person_svg).write(input_message)
    add_message(input_message)
    