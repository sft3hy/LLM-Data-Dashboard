import streamlit as st
st.set_page_config(page_icon="🤖", layout="centered")

import streamlit as st
from utils.code_editor import code_refiner, correct_code
from config import BOT_RESPONSE_REFINED, CODE_REFINER_MODEL
from random import randint
import os
from utils.message_utils import add_user_message, add_assistant_message
from utils.misc import get_last_dashboard, correct_code_remotely

FILENAME = os.path.basename(__file__)

# Load SVG assets
with open("data/resources/doggie.svg", "r") as bot_file:
    bot_svg = bot_file.read()
with open("data/resources/person.svg", "r") as person_file:
    person_svg = person_file.read()

# Placeholders for dynamic updates
user_chat_placeholder = st.empty()
code_execution_placeholder = st.empty()
code_explanation_placeholder = st.empty()

# Function to update sections
def update_sections(user_message, generated_code, bot_response, code_expander_text):
    # Update user chat section

    with user_chat_placeholder.container():
        st.chat_message("user", avatar=person_svg).write(user_message)

    # Update code execution section
    with code_execution_placeholder.container():
        try:
            exec(generated_code, {}, {})
        except Exception as e:
            st.markdown("### Error")
            st.error(f"An error occurred: {e}")

    # Update code explanation section
    with code_explanation_placeholder.container():
        assistant_message = st.chat_message("assistant", avatar=bot_svg)
        assistant_message.write(bot_response)
        assistant_message.expander(code_expander_text).code(generated_code, language="python")

prev_messages = get_last_dashboard(FILENAME)
prev_user_message = prev_messages[-2]
prev_bot_message = prev_messages[-1]
update_sections(prev_user_message['message_contents'], prev_bot_message['assistant_code'], prev_bot_message['message_contents'], prev_bot_message['assistant_code_expander'])

# Add the chat input field
input_message = st.chat_input(placeholder="Show the data as a histogram instead of a line chart")

if 'user_info' in st.session_state and st.session_state.user_info and st.session_state.user_info['email']:
    user_email = st.session_state.user_info['email']
else:
    user_email = 'no_email'

if input_message:
    # Retrieve the previous code
    previous_code = get_last_dashboard(FILENAME)[-1]['assistant_code']

    # Generate refined code
    context = """
Snippet(s) of the user's files: 'user_uploaded_files/fatalities_isr_pse_conflict_2000_to_2023.csv': "Columns and Data Types:\n  - name: string\n  - date_of_event: date\n  - age: float64\n  - citizenship: categorical\n  - event_location: string\n  - event_location_district: string\n  - event_location_region: categorical\n  - date_of_death: date\n  - gender: categorical\n  - took_part_in_the_hostilities: categorical\n  - place_of_residence: string\n  - place_of_residence_district: string\n  - type_of_injury: string\n  - ammunition: string\n  - killed_by: categorical\n  - notes: string\n\nPreview of Rows:\n                                       name date_of_event  age citizenship    event_location event_location_district event_location_region date_of_death gender took_part_in_the_hostilities place_of_residence place_of_residence_district type_of_injury      ammunition               killed_by                                                                                                                                                                                                                                                                                                                                                                                                     notes\n'Abd a-Rahman Suleiman Muhammad Abu Daghash    2023-09-24 32.0 Palestinian    Nur Shams R.C.                 Tulkarm             West Bank    2023-09-24      M                          NaN     Nur Shams R.C.                     Tulkarm        gunfire live ammunition Israeli security forces                                                  Fatally shot by Israeli forces while standing on the roof of his home, watching clashes that erupted between them and young men after the forces entered the camp. During the forces’ incursion into the camp, another Palestinian was killed while fleeing the forces. According to the IDF Spokesperson, a soldier was moderately injured by shrapnel.\n       Usayed Farhan Muhammad 'Ali Abu 'Ali    2023-09-24 21.0 Palestinian    Nur Shams R.C.                 Tulkarm             West Bank    2023-09-24      M                          NaN     Nur Shams R.C.                     Tulkarm        gunfire live ammunition Israeli security forces Fatally shot by Israeli forces while trying to flee them after watching clashes that erupted after they entered the camp and included a fire exchange. Abu ‘Ali was a Hamas military wing operative. During the forces’ incursion into the camp, another Palestinian was killed while standing on the roof of his house. According to the IDF Spokesperson, a soldier was moderately injured by shrapnel.\n           'Abdallah 'Imad Sa'ed Abu Hassan    2023-09-22 16.0 Palestinian          Kfar Dan                   Jenin             West Bank    2023-09-22      M                          NaN           al-Yamun                       Jenin        gunfire live ammunition Israeli security forces                                                                                                                                                                                                         Fatally shot by soldiers while firing at them with an improvised gun during a fire exchange that erupted after they entered the village. Abu Hassan was an Islamic Jihad military wing operative.\n           Durgham Muhammad Yihya al-Akhras    2023-09-20 19.0 Palestinian 'Aqbat Jaber R.C.                 Jericho             West Bank    2023-09-20      M                          NaN  'Aqbat Jaber R.C.                     Jericho        gunfire live ammunition Israeli security forces                                                                                                                                                                                                                        Shot in the head by Israeli forces while throwing stones at them in clashes that erupted after they entered the camp and during which explosive devices were thrown at the forces.\n               Raafat 'Omar Ahmad Khamaisah    2023-09-19 15.0 Palestinian        Jenin R.C.                   Jenin             West Bank    2023-09-19      M                          NaN              Jenin                       Jenin        gunfire live ammunition Israeli security forces                        Wounded by soldiers’ gunfire after running away from them as they entered the camp. Soldiers also fired at a man who tried to evacuate him but did not hit him. Khamaiseh subsequently died of his wounds. Two Islamic Jihad military wing operatives were also killed in the incident. Another operative was wounded by the shrapnel and died of his wounds on 20 September 2023."
These are the file path(s): ['user_uploaded_files/fatalities_isr_pse_conflict_2000_to_2023.csv']"""
    refined_code = code_refiner(
        previous_code,
        f"{input_message} {context}"
    )
    corrected_code = correct_code_remotely(refined_code, "fix any errors", FILENAME)

    # Generate bot response
    bot_response = BOT_RESPONSE_REFINED[randint(0, len(BOT_RESPONSE_REFINED) - 1)]
    code_expander_text = f"View {CODE_REFINER_MODEL} refined dashboard code"

    # Update UI sections
    update_sections(input_message, corrected_code, bot_response, code_expander_text)

    # Save messages
    add_user_message(file_path=FILENAME, message_contents=input_message, user_id=user_email)
    add_assistant_message(
        file_path=FILENAME,
        message_contents=bot_response,
        assistant_code_expander=code_expander_text,
        assistant_code=corrected_code,
        assistant_code_top=f"# Dashboard generated for your request: '{input_message}'"
    )

    