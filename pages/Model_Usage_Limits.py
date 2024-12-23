import streamlit as st
st.set_page_config(page_title="Model use limits", page_icon="🔢", layout="centered")

st.title("Current model usage limits")
limits_data = [
    {"Model": "gpt-4o", "Daily Calls": 50},
    {"Model": "gpt-4o-mini", "Daily Calls": 150},
    {"Model": "gemma2-9b-it", "Daily Calls": 14400},
    {"Model": "llama-3.3-70b-versatile", "Daily Calls": 1000},
    {"Model": "llama3-70b-8192", "Daily Calls": 14400},
    {"Model": "mixtral-8x7b-32768", "Daily Calls": 14400}
]

st.dataframe(limits_data, use_container_width=False)