from streamlit_folium import folium_static
import streamlit as st
st.set_page_config(page_icon="🤖", layout="centered")
import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

# Load data
file_path = 'user_uploaded_files/russia_losses.json'
with open(file_path, 'r') as f:
    data = json.load(f)

# Convert to DataFrame
losses = pd.DataFrame(data['losses'])

# Convert date to datetime and count losses per day
losses['date'] = pd.to_datetime(losses['date'])
daily_losses = losses.groupby(['date', 'status']).size().unstack(fill_value=0)

# Streamlit dashboard
st.title('Daily Equipment Losses in Russia')
status_filter = st.multiselect('Select Status', options=daily_losses.columns.tolist(), default=daily_losses.columns.tolist())

# Filter data based on selected status
filtered_data = daily_losses[status_filter]

# Plotting
st.subheader('Bar Chart of Daily Equipment Losses')
st.bar_chart(filtered_data)