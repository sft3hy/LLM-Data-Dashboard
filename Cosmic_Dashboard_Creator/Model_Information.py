import streamlit as st
import json
import pandas as pd

# Path to the JSON file that keeps track of model usage
FILE_PATH = "data/model_counts.json"

# Model limits
MODEL_LIMITS = [
    {"Model": "gpt-4o", "Daily Calls": 50},
    {"Model": "gpt-4o-mini", "Daily Calls": 150},
    {"Model": "gemini-2.0-flash-exp", "Daily Calls": 1500},
    {"Model": "gemini-1.5-flash", "Daily Calls": 1500},
    {"Model": "llama-3.3-70b-versatile", "Daily Calls": 1000},
    {"Model": "llama-3.3-70b-versatile", "Daily Calls": 1000},
    {"Model": "llama-3.1-70b-versatile", "Daily Calls": 1000},
    {"Model": "llama3-70b-8192", "Daily Calls": 14400},
    {"Model": "gemma2-9b-it", "Daily Calls": 14400},
    {"Model": "mixtral-8x7b-32768", "Daily Calls": 14400},
]


# Function to load the JSON file
def load_model_counts(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Initialize with zeros if the file doesn't exist
        initial_data = {model["Model"]: 0 for model in MODEL_LIMITS}
        with open(file_path, "w") as file:
            json.dump(initial_data, file, indent=4)
        return initial_data


# Load the model counts
model_counts = load_model_counts(FILE_PATH)
# Prepare data for the dataframe
data = []
for model in MODEL_LIMITS:
    model_name = model["Model"]
    daily_limit = model["Daily Calls"]
    calls_today = model_counts.get(model_name, 0)
    calls_left = max(0, daily_limit - calls_today)
    data.append(
        {
            "Model Name": model_name,
            "Daily Call Limit": daily_limit,
            "Calls Today": calls_today,
            "Calls Left Today": calls_left,
        }
    )

# Convert to a dataframe
df = pd.DataFrame(data)

# Streamlit app configuration
st.set_page_config(page_title="Model use limits", page_icon="🔢", layout="centered")
st.title("Model Information")
st.write(
    "The dashboard creator uses a combination of OpenAI, Groq, and Google Large Language Models. "
    "The OpenAI models are accessed free via GitHub Marketplace, and the Groq models are accessed "
    "free via the Groq API. The Google gemini models are accessed via the free tier of Google AI Studio and Google Cloud."
)
st.markdown("[**Groq**](https://groq.com/)", unsafe_allow_html=True)
st.markdown(
    "[**OpenAI**](https://openai.com/index/hello-gpt-4o/)", unsafe_allow_html=True
)
st.markdown(
    "[**Google AI Studio**](https://aistudio.google.com/prompts/new_chat)",
    unsafe_allow_html=True,
)

# Display limits and usage
st.title("Current Model Usage Limits")
st.dataframe(df)
