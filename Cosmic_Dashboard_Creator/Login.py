import streamlit as st
from streamlit_auth0 import login_button
import os

st.set_page_config("Login", page_icon=":material/login:")

# Add a login button
user_info = login_button(
    domain=os.environ.get("AUTH0_DOMAIN"),
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    key=os.environ.get("AUTH0_CLIENT_SECRET"),
)

# Initialize session state for user info
if "user_info" not in st.session_state:
    st.session_state.user_info = None


# Update session state with user info if logged in
if user_info:
    print(user_info)
    st.session_state.user_info = user_info

# Display appropriate content based on login state
if st.session_state.user_info:
    st.write(f"Welcome {st.session_state.user_info['name']}!")
    st.write("You are logged in.")
else:
    st.write("Please log in to continue.")
