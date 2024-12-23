from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import json
import os

# Load the data from the JSON file
user_uploaded_files = 'user_uploaded_files'
with open(os.path.join(user_uploaded_files, 'russia_losses.json')) as f:
    data = json.load(f)

# Convert the data into a pandas dataframe
df = pd.json_normalize(data, 'losses')

# Convert the 'date' column into a datetime format
df['date'] = pd.to_datetime(df['date'])

# Create a new column 'week' to extract the week number from the date
df['week'] = df['date'].dt.isocalendar().week

# Create a pivot table to calculate the weekly losses split by type
pivot_table = df.pivot_table(index=['week'], columns=['type'], values='status', aggfunc='count')

# Set the Streamlit title, description and display the pivot table as a bar chart
st.title('Weekly Losses Split by Type')
st.write('This dashboard shows the weekly losses split by type for the Russian military.')
st.bar_chart(pivot_table)