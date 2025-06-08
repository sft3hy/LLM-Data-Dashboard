from config import DASHBOARD_REFINER_SUGGESTIONS
from random import randint


def output_refined_dashboard(file_context: str):
    empty = {}
    recommendation = DASHBOARD_REFINER_SUGGESTIONS[
        randint(0, len(DASHBOARD_REFINER_SUGGESTIONS) - 1)
    ]

    REFINER_BAR = f"""
import streamlit as st
from utils.code_editor import code_refiner, correct_code, get_file_messages
from config import BOT_RESPONSE_REFINED, ALL_MODELS
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

previous_messages = get_file_messages(FILENAME)

selected_model = st.sidebar.selectbox(
            "LLM for code refining:",
            options = ALL_MODELS,
            index=ALL_MODELS.index("llama-3.3-70b-versatile"),
        )
view_old = st.sidebar.button("View dashboard history")
hide_old = st.sidebar.button("Hide dashboard history")
if view_old and not hide_old:
    for message in previous_messages:
        if message['role'] == 'user':
            st.chat_message("user", avatar=person_svg).write(message['message_contents'])
        else:
            try:
                exec(message['assistant_code'], {empty})
            except Exception as e:
                st.markdown("### Error")
                st.error(f"An error occurred: {{e}}")

        # Update code explanation section
            assistant_message = st.chat_message("assistant", avatar=bot_svg)
            assistant_message.write(message['message_contents'])
            assistant_message.expander(message['assistant_code_expander']).code(message['assistant_code_top']+message['assistant_code'], language="python")
            st.divider()

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
            exec(generated_code, {empty})
        except Exception as e:
            st.markdown("### Error")
            st.error(f"An error occurred: {{e}}")

    # Update code explanation section
    with code_explanation_placeholder.container():
        assistant_message = st.chat_message("assistant", avatar=bot_svg)
        assistant_message.write(bot_response)
        assistant_message.expander(code_expander_text).code(generated_code, language="python")

prev_messages = get_last_dashboard(FILENAME)
prev_user_message = prev_messages[-2]
prev_bot_message = prev_messages[-1]
if not view_old:
    update_sections(prev_user_message['message_contents'], prev_bot_message['assistant_code'], prev_bot_message['message_contents'], prev_bot_message['assistant_code_expander'])

# Add the chat input field
input_message = st.chat_input(placeholder="{recommendation}")

if 'user_info' in st.session_state and st.session_state.user_info and st.session_state.user_info['email']:
    user_email = st.session_state.user_info['email']
else:
    user_email = 'no_email'

if input_message:
    # Retrieve the previous code
    previous_code = get_last_dashboard(FILENAME)[-1]['assistant_code']

    # Generate refined code
    context = \"\"\"{file_context}\"\"\"
    refined_code = code_refiner(
        previous_code,
        f"{{input_message}} {{context}}",
        model=selected_model
    )
    corrected_code = correct_code_remotely(refined_code, "fix any errors", FILENAME)

    # Generate bot response
    bot_response = BOT_RESPONSE_REFINED[randint(0, len(BOT_RESPONSE_REFINED) - 1)]
    code_expander_text = f"View {{selected_model}} refined dashboard code"

    # Update UI sections
    update_sections(input_message, corrected_code, bot_response, code_expander_text)

    # Save messages
    add_user_message(file_path=FILENAME, message_contents=input_message, user_id=user_email)
    add_assistant_message(
        file_path=FILENAME,
        message_contents=bot_response,
        assistant_code_expander=code_expander_text,
        assistant_code=corrected_code,
        assistant_code_top=f"# Dashboard generated for your request: '{{input_message}}'"
    )

    """
    return REFINER_BAR
