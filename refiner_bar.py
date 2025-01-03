from config import CODE_REFINER_MODEL, DASHBOARD_REFINER_SUGGESTIONS
from random import randint

def output_refined_dashboard(existing_code: str):
    empty = {}
    recommendation = DASHBOARD_REFINER_SUGGESTIONS[randint(0, len(DASHBOARD_REFINER_SUGGESTIONS)-1)]

    REFINER_BAR = f"""

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
    \"\"\"Handles input from the chat input component.\"\"\"
    if input_message.strip():

        # Existing code for the dashboard
        existing_code = \"\"\"{existing_code}\"\"\"

        # Refine code based on input
        new_code = code_refiner(existing_code, input_message)

        user_requests = f\"\"\"# Dashboard generated for your request: "{{input_message}}"\n\"\"\"

        # Optionally execute the new code (be cautious of dynamic exec)
        try:
            exec(new_code, {empty})
        except Exception as e:
            print("ERROR:", e)
            correct_code(new_code, e)
            st.toast("Too many errors, try a different dashboard modification")

        # Display assistant response
        assistant_message = st.chat_message("assistant", avatar=bot_svg)
        assistant_message.write(BOT_RESPONSE_REFINED[randint(0, len(BOT_RESPONSE_REFINED)-1)])
        assistant_message.expander("View {CODE_REFINER_MODEL} refined dashboard code").code(f\"\"\"{{user_requests}}{{new_code}}\"\"\", language="python")

# Add the chat input field
input_message = st.chat_input(placeholder="{recommendation}")


if input_message:
    st.chat_message("user", avatar=":material/person:").write(input_message)
    add_message(input_message)
    """
    return REFINER_BAR