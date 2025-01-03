streamlit_sys_prompt = {
                    "role": "system",
                    "content": """You are a dashboard-creating assistant. Based on user input, write Streamlit code to visualize requested insights using provided data,
                    filenames, and file paths. Include an informative st.title() in the script. Output only the Streamlit code.""",
                }

code_corrector_sys_prompt = {
    "role": "system",
    "content": """You are a code-correcting assistant. Given Streamlit code and its error, fix the code to resolve the issue,
    considering its intended functionality. Output only the corrected code."""
}

code_refiner_sys_prompt = {
    "role": "system",
    "content": """You are a code-refining assistant. Given Streamlit code and its intended functionality, refine it as requested.
    Output only the updated code, with comments explaining your changes."""
}

normal_sys_prompt = {
    "role": "system",
    "content": """You answer questions concisely"""
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
    "Here is the refined code based on your request:",
    "I have refined the code to meet your requirements:",
    "The code has been updated to reflect your request:",
    "Here is the updated code tailored to your input:",
    "The following code has been adjusted as per your request:",
    "Here's the code modified according to your preferences:",
    "I've made the requested updates to the code:",
    "Your requested refinements have been applied to the code:",
    "Here's the adjusted code that aligns with your input:",
    "I've implemented changes to the code based on your feedback:",
    "Here is the refined version of the code:",
    "The code has been revised as per your specifications:",
    "Here's the code updated to incorporate your request:",
    "I've tailored the code to match your requirements:",
    "Here's the refined and updated code:",
    "I've customized the code to reflect your input:",
    "Here's the optimized code based on your feedback:",
    "The code has been modified to align with your request:",
    "I've adjusted the code as per your suggestions:",
    "Here's the code that incorporates your changes:",
]


MODEL_LIMITS = [
    {"Model": "gpt-4o", "Daily Calls": 50},
    {"Model": "gpt-4o-mini", "Daily Calls": 150},
    {"Model": "llama-3.3-70b-versatile", "Daily Calls": 1000},
    {"Model": "llama-3.3-70b-specdec", "Daily Calls": 1000},
    {"Model": "llama-3.1-70b-versatile", "Daily Calls": 1000},
    {"Model": "llama3-70b-8192", "Daily Calls": 14400},
    {"Model": "gemma2-9b-it", "Daily Calls": 14400},
    {"Model": "mixtral-8x7b-32768", "Daily Calls": 14400},
]

GROQ_MODELS = ["llama-3.3-70b-versatile",
               "llama-3.3-70b-specdec",
               "llama-3.1-70b-versatile",
               "llama3-70b-8192",
               "gemma2-9b-it",
               "mixtral-8x7b-32768"
               ]


"""
llama-3.2-90b-vision-preview
llama-guard-3-8b
"""

CODE_CORRECTION_TRIES = 3
CODE_CORRECTOR_MODEL = "llama3-70b-8192"
CODE_REFINER_MODEL = "llama3-70b-8192"
