from streamlit_folium import folium_static
from streamlit_folium import st_folium
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the dashboard
st.title("Distribution of Star Temperatures Across Different Spectral Classes")

# Load the data
file_path = 'user_uploaded_files/star_dataset.csv'

# Check if the file exists and load the data
try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("File not found. Please upload the star dataset.")
    st.stop()  # Stop execution if the file is not found

# Create a box plot of Temperature__K_ by Spectral_Class
fig, ax = plt.subplots()

# Ensure that the unique spectral classes are sorted for better visualization
unique_classes = sorted(data['Spectral_Class'].unique())
ax.boxplot([data.loc[data['Spectral_Class'] == class_name, 'Temperature__K_'] for class_name in unique_classes], labels=unique_classes)

ax.set_xlabel('Spectral Class')
ax.set_ylabel('Temperature (K)')
ax.set_title('Distribution of Star Temperatures Across Different Spectral Classes')

# Display the plot
st.pyplot(fig)