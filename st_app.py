import streamlit as st
import os

# List all files ending with .py in the directory
folder_name = "Your_Dashboards"
python_files = [f for f in os.listdir(folder_name) if f.endswith('.py')]

# Sort the files alphabetically
python_files.sort()

count = 0
dashboard_pages = []
for file in python_files:
    cleaned = file.replace('_', ' ').replace('.py', '')
    dashboard_pages.append(st.Page(
        f"{folder_name}/{file}",
        title=cleaned,
        icon=":material/smart_toy:",
        )
    )
    count += 1


# Page configuration
creator = st.Page("Cosmic_Dashboard_Creator/Dashboard_Creator.py", title="Dashboard Creator", icon=":material/dashboard:", default=True)
about = st.Page(
    "Cosmic_Dashboard_Creator/About.py", title="About", icon=":material/waving_hand:",
)
model_info = st.Page(
    "Cosmic_Dashboard_Creator/Model_Information.py", title="Model Info", icon=":material/info:"
)

pg = st.navigation(
{
    "Cosmic Dashboard Creator": [creator, about, model_info],
    "Your Dashboards": dashboard_pages,
}
)
pg.run()