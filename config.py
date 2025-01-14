from datetime import datetime
import os
import socket
import uvicorn
import threading

streamlit_sys_prompt = """You are a senior data scientist dashboard creator. Based on user input, write Streamlit code to visualize requested insights using provided data,
                    filenames, and file paths. Include an informative st.title() in the script. Prioritize the following native streamlit elements: 
                    st.area_chart, st.bar_chart, st.line_chart, st.map, st.scatter_chart, st.altair_chart, st.bokeh_chart, st.graphviz_chart, st.plotly_chart, st.pydeck_chart, st.pyplot, st.vega_lite_chart. 
                    Output only the Streamlit code."""

code_corrector_sys_prompt = """You are a code-correcting assistant. Given Streamlit code and its error, fix the code to resolve the issue,
    considering its intended functionality. Output only the corrected code."""

code_refiner_sys_prompt = """You are a senior data scientist dashboard refiner. Given Streamlit code and its intended functionality, refine it as requested.
    Output only the updated code, with comments explaining your changes."""

normal_sys_prompt = """You answer questions concisely"""

summarizer_sys_prompt = {
    "role": "system",
     "content": """
You are an experienced data analyst that can annotate datasets. Your instructions are as follows:
i) ALWAYS generate the name of the dataset and the dataset_description
ii) ALWAYS generate a field description.
iii.) ALWAYS generate a semantic_type (a single word) for each field given its values e.g. company, city, number, supplier, location, gender, longitude, latitude, url, ip address, zip code, email, etc
You must return an updated JSON dictionary without any preamble or explanation.
"""
}

DASHBOARD_REFINER_SUGGESTIONS = [
    "I want a pie chart instead of a bar chart",
    "Zoom out the map to see more data points",
    "Plot the data over a longer time frame",
    "Add a trend line to the chart",
    "Filter the data to show only the top 10 categories",
    "Switch to a heatmap for better data density visualization",
    "Add annotations for key events on the timeline",
    "Include a drill-down feature to explore specific data subsets",
    "Show cumulative totals instead of daily changes",
    "Use a scatter plot to visualize correlations",
    "Add percentage labels to the pie chart",
    "Group the data by region instead of category",
    "Change the color scheme to be more accessible",
    "Add interactive tooltips with detailed data on hover",
    "Show the data as a histogram instead of a line chart",
    "Sort the bar chart in descending order",
    "Include a comparison against last year's data",
    "Enable a slider to adjust the time range dynamically",
    "Highlight the outliers in the dataset",
    "Provide export options for the dashboard data",
]

BOT_RESPONSE_REFINED = [
    "Here is the refined dashboard based on your request",
    "I have refined the dashboard to meet your requirements",
    "The dashboard has been updated to reflect your request",
    "Here is the updated dashboard tailored to your input",
    "The following dashboard has been adjusted as per your request",
    "Here's the dashboard modified according to your preferences",
    "I've made the requested updates to the dashboard",
    "Your requested refinements have been applied to the dashboard",
    "Here's the adjusted dashboard that aligns with your input",
    "I've implemented changes to the dashboard based on your feedback",
    "Here is the refined version of the dashboard",
    "The dashboard has been revised as per your specifications",
    "Here's the dashboard updated to incorporate your request",
    "I've tailored the dashboard to match your requirements",
    "Here's the refined and updated dashboard",
    "I've customized the dashboard to reflect your input",
    "Here's the optimized dashboard based on your feedback",
    "The dashboard has been modified to align with your request",
    "I've adjusted the dashboard as per your suggestions",
    "Here's the dashboard that incorporates your changes",
]


MODEL_LIMITS = [
    {"Model": "gpt-4o", "Daily Calls": 50},
    {"Model": "gpt-4o-mini", "Daily Calls": 150},
    {"Model": "gemini-2.0-flash-exp", "Daily Calls": 1500},
    {"Model": "gemini-1.5-flash", "Daily Calls": 1500},
    {"Model": "llama-3.3-70b-versatile", "Daily Calls": 1000},
    {"Model": "llama-3.3-70b-specdec", "Daily Calls": 1000},
    {"Model": "llama-3.1-70b-versatile", "Daily Calls": 1000},
    {"Model": "llama3-70b-8192", "Daily Calls": 14400},
    {"Model": "gemma2-9b-it", "Daily Calls": 14400},
    {"Model": "mixtral-8x7b-32768", "Daily Calls": 14400},
]

GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.3-70b-specdec",
    "llama-3.1-70b-versatile",
    "llama3-70b-8192",
    "gemma2-9b-it",
    "mixtral-8x7b-32768"
]

GOOGLE_MODELS = [
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
]

OPENAI_MODELS = [
    "gpt-4o",
    "gpt-4o-mini"
]

ALL_MODELS = OPENAI_MODELS + GOOGLE_MODELS + GROQ_MODELS


"""
llama-3.2-90b-vision-preview
llama-guard-3-8b
"""

CODE_CORRECTION_TRIES = 3
CODE_CORRECTOR_MODEL = "llama3-70b-8192"
CODE_REFINER_MODEL = "llama3-70b-8192"
STORAGE_FILE = "data/messages.json"
GENERATED_FILES_DIR = "Your_Dashboards"

AZURE_API_KEY=os.environ.get("GH_ACCESS_TOKEN", None)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", None)
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY", None)

from kaggle.api.kaggle_api_extended import KaggleApi


def setup_kaggle_api():
    """
    Sets up the Kaggle API using the Kaggle JSON credentials file.
    
    Ensure you have the 'kaggle.json' file in your home directory's '.kaggle' folder
    or in an environment variable.
    """
    try:
        # Initialize and authenticate the Kaggle API
        api = KaggleApi()
        api.authenticate()
        # print("Kaggle API setup successful.")
        return api
    except Exception as e:
        raise RuntimeError(f"Error setting up Kaggle API: {e}")
    
def get_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
KAGGLE_API = setup_kaggle_api()


def is_port_in_use(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def run_uvicorn():
    if not is_port_in_use("127.0.0.1", 8000):
        uvicorn.run("error_correction_service:app", host="127.0.0.1", port=8000, reload=False)
    else:
        print("Server already running on port 8000. Skipping start.")

uvicorn_thread = threading.Thread(target=run_uvicorn, daemon=True)
uvicorn_thread.start()
print('Uvicorn started running microservice')