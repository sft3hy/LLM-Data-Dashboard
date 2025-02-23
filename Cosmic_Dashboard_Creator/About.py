import streamlit as st

# About Page
st.set_page_config(page_title="About", page_icon="👋", layout="centered")
st.markdown("""
# About Cosmic Dashboards 📊

Welcome to Cosmic Dashboards, your one-stop solution for AI powered data visualization!  
This app is designed to make dashboard creation easier, faster, and more accessible for everyone, whether you're a beginner or an expert.

---

## How to use the tool 🚀

- **Step 1**: Drag and drop your data file (KML, JSON, GeoJSON, CSV, Shapefile zip folder)
- **Step 2**: Write your dashboard request  
- **Step 3**: Navigate to your newly created dashboard on the left menu bar

---


## Behind the Scenes 🤖

This app was built using [**Streamlit**](https://streamlit.io/), a modern framework for creating data-driven web applications. It integrates powerful libraries like:  
- **openai**, **groq**, and **gemini**: Your selected model generates streamlit code based on your dashboard request
- **geopandas**: useful for analyzing geospatial and temporal data
- **folium**: map displaying library 

---

## About the Developer 🛠️

Hi, I'm Sam Townsend! 👋  
I'm passionate about data visualization, web development, and generative AI and have created this app to help others explore their own data and automate dashboard creation.  

Feel free to connect with me on:  
- [**My Website**](https://sft3hy.github.io/sam-townsend)
- [**GitHub**](https://github.com/sft3hy)  
- [**LinkedIn**](https://linkedin.com/in/samuel-townsend1)  

---

## Feedback & Support 📨

Your feedback is welcome!  
If you encounter issues or have suggestions, please reach out at smaueltown@gmail.com.  

---

*Thank you for using Cosmic Dashboards!* 🎉
""")

st.html("""<div style="text-align: center; font-size: smaller;">
                <a href="https://groq.com" target="_blank" rel="noopener noreferrer">
                    <img src="https://groq.com/wp-content/uploads/2024/03/PBG-mark1-color.svg"
                    style="width: 100px; height: auto; display: block; margin: auto;"
                    alt="Powered by Groq for fast inference."/>
                </a>
            </div>
"""
)