import subprocess
import sys
import streamlit as st

def ensure_library_installed(library_name):
    """
    Ensures a Python library is installed in the environment.
    Installs the library if it is not already present.

    Parameters:
        library_name (str): The name of the library to check and install.
    """
    try:
        __import__(library_name)
    except ImportError:
        st.warning(f"Installing missing library: {library_name}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])
