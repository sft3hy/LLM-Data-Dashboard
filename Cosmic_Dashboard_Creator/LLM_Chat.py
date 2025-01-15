import streamlit as st
from config import normal_sys_prompt, ALL_MODELS, OPENAI_MODELS, GROQ_MODELS, AZURE_API_KEY, GOOGLE_MODELS, GOOGLE_API_KEY
from utils.model_caller import call_model
from groq import Groq
import os
from openai import AzureOpenAI, OpenAI
from utils.model_call_tracker import update_model_count


col1, col2 = st.columns(2)
with col2:
    st.markdown("LLM Temperature", help="Set the model temperature. 0 = more logical, 2.0 = more creative")
    temperature = st.slider(
                "A",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                label_visibility="collapsed"
                )
with col1:
    selected_model = st.selectbox(
                "Select an AI chatbot:",
                options = ALL_MODELS,
                index=ALL_MODELS.index("llama-3.3-70b-specdec"),
            )

user_text = st.chat_input("Ask me anything")

if 'user_messages' not in st.session_state:
    st.session_state.user_messages = []
if 'bot_messages' not in st.session_state:
    st.session_state.bot_messages = []

# Delete all session state messages
# st.session_state.user_messages = []
# st.session_state.bot_messages = []


if "user_messages" in st.session_state and "bot_messages" in st.session_state:
    for user_message, bot_message in zip(st.session_state.user_messages, st.session_state.bot_messages):
        st.chat_message("human").write(user_message)
        st.chat_message("ai").write(bot_message)

client = ""
if selected_model in OPENAI_MODELS:
    client_args = {
        "api_key": AZURE_API_KEY,
        "api_version": "2024-10-21",
        "azure_endpoint": "https://models.inference.ai.azure.com",
    }
    # remove keys with None values
    client_args = {k: v for k,
                        v in client_args.items() if v is not None}
    client = AzureOpenAI(**client_args)
elif selected_model in GROQ_MODELS:
    client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
elif selected_model in GOOGLE_MODELS:
    client = OpenAI(
                api_key=GOOGLE_API_KEY,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )


def stream_groq(stream):
    for chunk in stream:
        text = chunk.choices[0].delta.content
        if text is not None and type(text) != "int":
            yield int

if temperature and selected_model and user_text is not None:
    st.chat_message("human").write(user_text)
    st.session_state['user_messages'].append(user_text)

    stream = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": normal_sys_prompt},
                {"role": "user", "content": user_text},
            ],
            stream=True,
        )
    response = ""
    print(selected_model)
    update_model_count(selected_model, increment=True)
    if selected_model in GROQ_MODELS:
        with st.chat_message("ai"):
            response = st.write_stream(stream_groq(stream))
    else:
        with st.chat_message("ai"):
            response = st.write_stream(stream)

    # st.chat_message("ai").write(response)
    st.session_state['bot_messages'].append(response)
