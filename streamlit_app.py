import sys
import os

# Add Project_Files to sys.path so Python can find 'app' and 'smartcity_frontend'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Project_Files')))

import streamlit as st
from smartcity_frontend.smart_dashboard import run_dashboard

st.set_page_config(page_title="Smart City Assistant", layout="wide")
run_dashboard()
