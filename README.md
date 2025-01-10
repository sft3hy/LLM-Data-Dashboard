# Drag-and-Drop Dashboard Generator

This repository contains a **Streamlit web app** that allows users to bring their own data in formats like **CSV**, **JSON**, **KML**, **Shapefile**, or **GeoJSON**. Using natural language requests, you can describe the kind of dashboard you'd like to generate, and the app will create it for you using an **LLM-powered engine**.

## Features

- **Drag-and-Drop Interface**: Upload your data files (KML, Shapefile, GeoJSON) directly into the app.  
- **Natural Language Dashboard Requests**: Describe the dashboard you want to create in plain language (e.g., "Create a bar chart of population by region").  
- **Streamlit Framework**: A clean and interactive UI built with Streamlit for quick and efficient visualization generation.  
- **LIDA Implementation**: Incorporates Microsoft's [LIDA (Language-Integrated Data Analysis)](https://microsoft.github.io/lida/) for advanced natural language understanding and dashboard creation.  

## How It Works

1. Upload your data file (supports CSV, JSON, KML, Shapefile, GeoJSON).  
2. Use the natural language input box to describe the dashboard or visualization you want.  
3. The app processes your request and dynamically generates the desired dashboard.  

## Prerequisites

- Python 3.8 or higher  
- Streamlit 1.15 or higher  

## Running the App

1. Clone this repository:
```bash
git clone https://github.com/sft3hy/LLM-Data-Dashboard.git
cd drag-and-drop-dashboard-generator
```
2. Install dependencies using the following command:  
```bash
pip install -r requirements.txt
```
3. Start the Streamlit app:
```bash
streamlit run st_app.py
```

## Screenshots

## Built with
- [Streamlit](https://streamlit.io/)
- [LIDA](https://microsoft.github.io/lida/)
- [Groq](https://groq.com/)
- [Google AI Studio](https://aistudio.google.com/prompts/new_chat)
- [Github Marketplace](https://github.com/marketplace)