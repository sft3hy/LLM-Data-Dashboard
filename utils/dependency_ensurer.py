import subprocess
import sys
import streamlit as st
import pkg_resources

def ensure_library_installed(library_name):
    """
    Ensures a Python library is installed in the environment.
    Installs the library if it is not already present and adds it to requirements.txt.

    Parameters:
        library_name (str): The name of the library to check and install.
    """
    try:
        # Try to import the library
        __import__(library_name)
    except ImportError:
        msg = st.toast(f"Adding new python library for dashboard: {library_name}")
        # Install the library using pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])

        # Get the installed library version
        dist = pkg_resources.get_distribution(library_name)
        package_version = f"{dist.project_name}=={dist.version}"

        # Update the requirements.txt file
        requirements_path = "../requirements.txt"  # Path to requirements.txt
        try:
            with open(requirements_path, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            lines = []

        # Check if the package is already in requirements.txt
        if not any(package_version.split("==")[0] in line for line in lines):
            with open(requirements_path, "a") as file:
                file.write(f"{package_version}\n")
            st.success(f"Added {package_version} to requirements.txt")

ensure_library_installed("plotly")
