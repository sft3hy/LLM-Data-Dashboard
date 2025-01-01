import streamlit as st
from config import MODEL_LIMITS

st.set_page_config(page_title="Model use limits", page_icon="🔢", layout="centered")
st.title("Model Information")
st.write("The dashboard creator uses a combination of OpenAI and Groq Large Language Models. The OpenAI models are accessed free via GitHub Marketplace, and the Groq models are accessed free via the Groq API.")
st.markdown("[**Groq**](https://groq.com/)", unsafe_allow_html=True)
st.markdown("[**OpenAI**](https://openai.com/index/hello-gpt-4o/)", unsafe_allow_html=True)

st.title("Current model usage limits")
limits_data = MODEL_LIMITS

st.dataframe(limits_data, use_container_width=False)