from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import json
import plotly.express as px

# Load the data
st.set_page_config(page_title="Combined Data Dashboard", page_icon=":robot_face:", layout="centered")


st.title("Combined Data Dashboard")

st.sidebar.title("Navigation")
menu = ["911 Calls", "Russia Losses: Vehicles", "Russia Losses: Equipment", "Russia Losses: Personnel"]
choice = st.sidebar.radio("Select Dataset", menu)

if choice == "911 Calls":
    st.header("911 Calls Dashboard")
    data_911 = pd.read_csv("user_uploaded_files/911.csv")
    
    st.write("Data Overview")
    st.write(data_911.head())
    
    # Common Calls Visualization
    data_911['Reason'] = data_911['title'].str.split(':').str[0]
    reason_count = data_911['Reason'].value_counts()
    fig = px.bar(reason_count, x=reason_count.index, y=reason_count.values, labels={"x": "Reason", "y": "Count"}, title="Most Common Reasons for 911 Calls")
    st.plotly_chart(fig)

    # Calls Over Time
    data_911['timeStamp'] = pd.to_datetime(data_911['timeStamp'])
    data_911['Hour'] = data_911['timeStamp'].dt.hour
    hour_count = data_911.groupby("Hour").size()
    fig = px.line(hour_count, x=hour_count.index, y=hour_count.values, labels={"x": "Hour of Day", "y": "Call Volume"}, title="911 Calls by Hour")
    st.plotly_chart(fig)

if choice == "Russia Losses: Vehicles":
    st.header("Russia Losses - Vehicle Analysis")
    data_vehicles = pd.read_csv("user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv")
    
    st.write("Data Overview")
    st.write(data_vehicles.head())
    
    # Vehicle Losses by Type
    vehicle_type_count = data_vehicles['vehicle_type'].value_counts()
    fig = px.bar(vehicle_type_count, x=vehicle_type_count.index, y=vehicle_type_count.values, labels={"x": "Vehicle Type", "y": "Count"}, title="Vehicle Losses by Type")
    st.plotly_chart(fig)

    # Losses Over Time
    data_vehicles['date'] = pd.to_datetime(data_vehicles['date'])
    losses_over_time = data_vehicles['date'].value_counts().sort_index()
    fig = px.line(losses_over_time, x=losses_over_time.index, y=losses_over_time.values, labels={"x": "Date", "y": "Losses"}, title="Vehicle Losses Over Time")
    st.plotly_chart(fig)

if choice == "Russia Losses: Equipment":
    st.header("Russia Losses - Equipment Analysis")
    data_equipment = pd.read_csv("user_uploaded_files/russia_losses_equipment.csv")
    
    st.write("Data Overview")
    st.write(data_equipment.head())
    
    # Equipment Losses Over Time
    data_equipment['date'] = pd.to_datetime(data_equipment['date'])
    fig = px.line(data_equipment, x="date", y="tank", labels={"date": "Date", "tank": "Tanks Lost"}, title="Tanks Lost Over Time")
    st.plotly_chart(fig)
    
    fig = px.line(data_equipment, x="date", y="aircraft", labels={"date": "Date", "aircraft": "Aircraft Lost"}, title="Aircraft Lost Over Time")
    st.plotly_chart(fig)

if choice == "Russia Losses: Personnel":
    st.header("Russia Losses - Personnel Analysis")
    data_personnel = pd.read_csv("user_uploaded_files/russia_losses_personnel.csv")
    
    st.write("Data Overview")
    st.write(data_personnel.head())
    
    # Personnel Losses Over Time
    data_personnel['date'] = pd.to_datetime(data_personnel['date'])
    fig = px.line(data_personnel, x="date", y="personnel", labels={"date": "Date", "personnel": "Personnel Lost"}, title="Personnel Lost Over Time")
    st.plotly_chart(fig)


import streamlit as st
from streamlit.components.v1 import html
from helpers.code_editor import code_refiner, correct_code
from streamlit_extras.sandbox import sandbox


def render_svg(svg_string):
    """Renders the given svg string."""
    c = st.container()
    with c:
        html(svg_string)

# Assuming the PNG is in the 'images' directory
user_svg = open("data/resources/doggie.svg", "r").read()
bot_svg = open("data/resources/user.svg", "r").read()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages with custom SVGs
def display_messages():
    for msg in st.session_state.messages:
        if msg["is_user"]:
            # User message with custom SVG
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-end; align-items: center; margin: 10px 0;">
                    <div style="max-width: 70%; padding: 10px; border-radius: 10px;">
                        {{msg["content"]}}
                    </div>
                    {{bot_svg}}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Bot message with custom SVG
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-start; align-items: center; margin: 10px 0;">
                    {{user_svg}}
                    <div style="max-width: 70%; padding: 10px; border-radius: 10px;">
                        {{msg["content"]}}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# Add the chat input area
new_dash_message = 'Check the top of the page for your new dashboard.'
def add_message():
    if st.session_state.input_message.strip():
        # Add user message
        st.session_state.messages.append({{"content": st.session_state.input_message, "is_user": True}})
        # refine already existing code
        new_code = code_refiner("""import streamlit as st
import pandas as pd
import json
import plotly.express as px

# Load the data
st.title("Combined Data Dashboard")

st.sidebar.title("Navigation")
menu = ["911 Calls", "Russia Losses: Vehicles", "Russia Losses: Equipment", "Russia Losses: Personnel"]
choice = st.sidebar.radio("Select Dataset", menu)

if choice == "911 Calls":
    st.header("911 Calls Dashboard")
    data_911 = pd.read_csv("user_uploaded_files/911.csv")
    
    st.write("Data Overview")
    st.write(data_911.head())
    
    # Common Calls Visualization
    data_911['Reason'] = data_911['title'].str.split(':').str[0]
    reason_count = data_911['Reason'].value_counts()
    fig = px.bar(reason_count, x=reason_count.index, y=reason_count.values, labels={"x": "Reason", "y": "Count"}, title="Most Common Reasons for 911 Calls")
    st.plotly_chart(fig)

    # Calls Over Time
    data_911['timeStamp'] = pd.to_datetime(data_911['timeStamp'])
    data_911['Hour'] = data_911['timeStamp'].dt.hour
    hour_count = data_911.groupby("Hour").size()
    fig = px.line(hour_count, x=hour_count.index, y=hour_count.values, labels={"x": "Hour of Day", "y": "Call Volume"}, title="911 Calls by Hour")
    st.plotly_chart(fig)

if choice == "Russia Losses: Vehicles":
    st.header("Russia Losses - Vehicle Analysis")
    data_vehicles = pd.read_csv("user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv")
    
    st.write("Data Overview")
    st.write(data_vehicles.head())
    
    # Vehicle Losses by Type
    vehicle_type_count = data_vehicles['vehicle_type'].value_counts()
    fig = px.bar(vehicle_type_count, x=vehicle_type_count.index, y=vehicle_type_count.values, labels={"x": "Vehicle Type", "y": "Count"}, title="Vehicle Losses by Type")
    st.plotly_chart(fig)

    # Losses Over Time
    data_vehicles['date'] = pd.to_datetime(data_vehicles['date'])
    losses_over_time = data_vehicles['date'].value_counts().sort_index()
    fig = px.line(losses_over_time, x=losses_over_time.index, y=losses_over_time.values, labels={"x": "Date", "y": "Losses"}, title="Vehicle Losses Over Time")
    st.plotly_chart(fig)

if choice == "Russia Losses: Equipment":
    st.header("Russia Losses - Equipment Analysis")
    data_equipment = pd.read_csv("user_uploaded_files/russia_losses_equipment.csv")
    
    st.write("Data Overview")
    st.write(data_equipment.head())
    
    # Equipment Losses Over Time
    data_equipment['date'] = pd.to_datetime(data_equipment['date'])
    fig = px.line(data_equipment, x="date", y="tank", labels={"date": "Date", "tank": "Tanks Lost"}, title="Tanks Lost Over Time")
    st.plotly_chart(fig)
    
    fig = px.line(data_equipment, x="date", y="aircraft", labels={"date": "Date", "aircraft": "Aircraft Lost"}, title="Aircraft Lost Over Time")
    st.plotly_chart(fig)

if choice == "Russia Losses: Personnel":
    st.header("Russia Losses - Personnel Analysis")
    data_personnel = pd.read_csv("user_uploaded_files/russia_losses_personnel.csv")
    
    st.write("Data Overview")
    st.write(data_personnel.head())
    
    # Personnel Losses Over Time
    data_personnel['date'] = pd.to_datetime(data_personnel['date'])
    fig = px.line(data_personnel, x="date", y="personnel", labels={"date": "Date", "personnel": "Personnel Lost"}, title="Personnel Lost Over Time")
    st.plotly_chart(fig)""", st.session_state.input_message)
        exec(new_code, {})
        st.session_state.messages.append({{"content": new_dash_message, "is_user": False}})
        st.session_state.input_message = ""


# Style the input box to stick at the bottom
st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] {{
        position: fixed;
        bottom: 0;
        width: 100%;
        z-index: 100;
        background-color: #ffffff;
        padding: 10px 20px;
        box-shadow: 0px -2px 5px rgba(0,0,0,0.1);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Display chat messages
display_messages()

# Create the input bar
with st.container():
    st.subheader("Dashboard Editor")
    st.text_input("Dashboard editor",
                key="input_message",
                on_change=add_message,
                placeholder="I want a pie chart instead of a bar chart",
                label_visibility="collapsed"
    )

st.subheader('')


st.markdown("""Dashboard generated for your request: \"Combined data dashboard\" """)
st.markdown("""On data: \"02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv\", \"911.csv\", \"russia_losses_personnel.csv\", \"russia_losses_equipment.csv\" """)

        
st.markdown("""gpt-4o generated code:""")
st.code("""import streamlit as st
import pandas as pd
import json
import plotly.express as px

# Load the data
st.title("Combined Data Dashboard")

st.sidebar.title("Navigation")
menu = ["911 Calls", "Russia Losses: Vehicles", "Russia Losses: Equipment", "Russia Losses: Personnel"]
choice = st.sidebar.radio("Select Dataset", menu)

if choice == "911 Calls":
    st.header("911 Calls Dashboard")
    data_911 = pd.read_csv("user_uploaded_files/911.csv")
    
    st.write("Data Overview")
    st.write(data_911.head())
    
    # Common Calls Visualization
    data_911['Reason'] = data_911['title'].str.split(':').str[0]
    reason_count = data_911['Reason'].value_counts()
    fig = px.bar(reason_count, x=reason_count.index, y=reason_count.values, labels={"x": "Reason", "y": "Count"}, title="Most Common Reasons for 911 Calls")
    st.plotly_chart(fig)

    # Calls Over Time
    data_911['timeStamp'] = pd.to_datetime(data_911['timeStamp'])
    data_911['Hour'] = data_911['timeStamp'].dt.hour
    hour_count = data_911.groupby("Hour").size()
    fig = px.line(hour_count, x=hour_count.index, y=hour_count.values, labels={"x": "Hour of Day", "y": "Call Volume"}, title="911 Calls by Hour")
    st.plotly_chart(fig)

if choice == "Russia Losses: Vehicles":
    st.header("Russia Losses - Vehicle Analysis")
    data_vehicles = pd.read_csv("user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv")
    
    st.write("Data Overview")
    st.write(data_vehicles.head())
    
    # Vehicle Losses by Type
    vehicle_type_count = data_vehicles['vehicle_type'].value_counts()
    fig = px.bar(vehicle_type_count, x=vehicle_type_count.index, y=vehicle_type_count.values, labels={"x": "Vehicle Type", "y": "Count"}, title="Vehicle Losses by Type")
    st.plotly_chart(fig)

    # Losses Over Time
    data_vehicles['date'] = pd.to_datetime(data_vehicles['date'])
    losses_over_time = data_vehicles['date'].value_counts().sort_index()
    fig = px.line(losses_over_time, x=losses_over_time.index, y=losses_over_time.values, labels={"x": "Date", "y": "Losses"}, title="Vehicle Losses Over Time")
    st.plotly_chart(fig)

if choice == "Russia Losses: Equipment":
    st.header("Russia Losses - Equipment Analysis")
    data_equipment = pd.read_csv("user_uploaded_files/russia_losses_equipment.csv")
    
    st.write("Data Overview")
    st.write(data_equipment.head())
    
    # Equipment Losses Over Time
    data_equipment['date'] = pd.to_datetime(data_equipment['date'])
    fig = px.line(data_equipment, x="date", y="tank", labels={"date": "Date", "tank": "Tanks Lost"}, title="Tanks Lost Over Time")
    st.plotly_chart(fig)
    
    fig = px.line(data_equipment, x="date", y="aircraft", labels={"date": "Date", "aircraft": "Aircraft Lost"}, title="Aircraft Lost Over Time")
    st.plotly_chart(fig)

if choice == "Russia Losses: Personnel":
    st.header("Russia Losses - Personnel Analysis")
    data_personnel = pd.read_csv("user_uploaded_files/russia_losses_personnel.csv")
    
    st.write("Data Overview")
    st.write(data_personnel.head())
    
    # Personnel Losses Over Time
    data_personnel['date'] = pd.to_datetime(data_personnel['date'])
    fig = px.line(data_personnel, x="date", y="personnel", labels={"date": "Date", "personnel": "Personnel Lost"}, title="Personnel Lost Over Time")
    st.plotly_chart(fig)""", language="python")
