import streamlit as st
import os
from auth0_component import login_button
from utils.misc import build_markup_for_logo, generate_pages

dashboard_pages = generate_pages()


# Page configuration
creator = st.Page(
    "Cosmic_Dashboard_Creator/Dashboard_Creator.py", title="Dashboard Creator", icon=":material/dashboard:", default=True, 
)
about = st.Page(
    "Cosmic_Dashboard_Creator/About.py", title="About", icon=":material/waving_hand:",
)
model_info = st.Page(
    "Cosmic_Dashboard_Creator/Model_Information.py", title="Model Info", icon=":material/info:"
)
kaggle = st.Page(
    "Cosmic_Dashboard_Creator/Kaggle_Downloader.py", title="Kaggle Downloader", icon="🦆"
)
lida = st.Page(
    "Cosmic_Dashboard_Creator/LIDA.py", title="LIDA", icon="📊"
)

pg = st.navigation(
{
    "Cosmic Dashboard Creator": [creator, about, model_info, kaggle, lida],
    "Your Dashboards": dashboard_pages,
}
)
pg.run()

# Get the Auth0 client ID and domain from environment variables
client_id = os.environ.get("AUTH0_CLIENT_ID")
domain = os.environ.get("AUTH0_DOMAIN")

# Use the login button to get user info
with st.sidebar:
    user_info = login_button(client_id, domain=domain)

# Store the user info in session state if it's not None
if user_info:
    st.session_state.user_info = user_info

# Check if user info exists in session state and display it
if "user_info" in st.session_state and user_info:
    with st.sidebar:
        st.write(f"Welcome, {user_info['name']}")


st.markdown(
    build_markup_for_logo("data/resources/logo.png"),
    unsafe_allow_html=True,
)