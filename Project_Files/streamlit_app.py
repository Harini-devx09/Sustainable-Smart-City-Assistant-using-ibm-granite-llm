import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import streamlit as st
from smart_dashboard import show_dashboard

def main():
    st.set_page_config(page_title="Smart City Assistant", layout="wide")
    st.title("🌆 Sustainable Smart City Assistant")

if __name__ == "__main__":
    main()
