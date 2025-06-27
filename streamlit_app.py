import streamlit as st
from smartcity_frontend.smart_dashboard import run_dashboard

# Set page configuration
st.set_page_config(page_title="Smart City Assistant", layout="wide")

# Run your dashboard
run_dashboard()
