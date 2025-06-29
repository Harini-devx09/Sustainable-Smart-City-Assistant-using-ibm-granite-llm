import streamlit as st
import requests
import os

# Set backend API base URL
API_URL = "https://smartcity-api.onrender.com"
st.write(f"🔗 Using API URL: `{API_URL}`")  # Debug info

st.set_page_config(page_title="Smart City Assistant", layout="wide")
st.title("🌆 Sustainable Smart City Assistant")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📘 Sustainability Report",
    "📄 Policy Summarizer",
    "📊 KPI Forecasting",
    "🔍 Anomaly Detection",
    "💬 Chat Assistant"
])

with tab1:
    st.header("📘 Generate Sustainability Report")
    uploaded = st.file_uploader("Upload Sustainability Report PDF", type="pdf")
    if uploaded and st.button("Generate Report"):
        try:
            files = {'file': uploaded}
            res = requests.post(f"{API_URL}/generate_report", files=files)
            if res.status_code == 200:
                st.success(res.json().get("report", "No content"))
            else:
                st.error(f"❌ Failed with status {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"🚫 Error: {str(e)}")

with tab2:
    st.header("📄 Summarize Government Policy")
    pdf = st.file_uploader("Upload Government Policy PDF", type="pdf", key="policy")
    if pdf and st.button("Summarize Policy"):
        try:
            files = {'file': pdf}
            res = requests.post(f"{API_URL}/summarize_policy", files=files)
            if res.status_code == 200:
                st.success(res.json().get("summary", "No summary"))
            else:
                st.error(f"❌ Failed with status {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"🚫 Error: {str(e)}")

with tab3:
    st.header("📊 Upload KPI CSV for Forecasting")
    csv = st.file_uploader("Upload KPI CSV", type="csv", key="kpi")
    if csv and st.button("Predict KPI"):
        try:
            files = {'file': csv}
            res = requests.post(f"{API_URL}/predict_kpi", files=files)
            if res.status_code == 200:
                st.json(res.json())
            else:
                st.error(f"❌ Failed with status {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"🚫 Error: {str(e)}")

with tab4:
    st.header("🔍 Anomaly Detection in KPI File")
    anomaly_csv = st.file_uploader("Upload KPI File (CSV)", type="csv", key="anomaly")
    if anomaly_csv and st.button("Detect Anomalies"):
        try:
            files = {'file': anomaly_csv}
            res = requests.post(f"{API_URL}/detect_anomalies", files=files)
            if res.status_code == 200:
                st.json(res.json())
            else:
                st.error(f"❌ Failed with status {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"🚫 Error: {str(e)}")

with tab5:
    st.header("🤖 Smart City Chat Assistant")
    prompt = st.text_input("Ask a question about your city:")
    if prompt and st.button("Ask Assistant"):
        try:
            res = requests.post(f"{API_URL}/ask-assistant/", json={"prompt": prompt})
            if res.status_code == 200:
                st.write("🧠 Response:", res.json().get("response", "No answer"))
            else:
                st.error(f"❌ Failed with status {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"🚫 Error: {str(e)}")
