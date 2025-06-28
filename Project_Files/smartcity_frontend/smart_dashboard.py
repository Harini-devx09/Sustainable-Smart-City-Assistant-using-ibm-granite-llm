import sys
import os

# Dynamically add 'Project_Files' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import streamlit as st
import requests
from fpdf import FPDF
import tempfile
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

st.set_page_config(page_title="🌆 Smart City Assistant", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .sidebar .sidebar-content { background-color: #eef5ff; }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        margin: 10px 0;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
        text-align: center;
        transition: all 0.3s ease-in-out;
    }
    .metric-card:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    .metric-label { font-size: 18px; color: #444; font-weight: 600; }
    .metric-value { font-size: 36px; font-weight: bold; color: #0077cc; }
    .metric-delta { font-size: 14px; color: green; }
    .section-card {
        background-color: #fff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.04);
        margin-bottom: 20px;
        transition: all 0.3s ease-in-out;
    }
    .section-card:hover {
        background-color: #f8faff;
    }
    </style>
""", unsafe_allow_html=True)

BASE_URL = "http://127.0.0.1:8000"

def convert_to_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp.name)
    return temp.name

with st.sidebar:
    selected = option_menu(
        menu_title="🚀 Smart City Assistant",
        options=[
            "🏠 Dashboard Summary",
            "🍃 Eco Tips",
            "📊 KPI Forecasting",
            "🔍 Anomaly Detection",
            "📘 Sustainability Report",
            "📄 Policy Summarizer",
            "🤖 Chat Assistant",
            "📋 Citizen Feedback" 
        ],
        icons=["house", "leaf", "bar-chart", "activity", "file-earmark-text", "file-earmark", "chat-dots", "file-text"],
        default_index=0,
        orientation="vertical"
    )

if selected == "🏠 Dashboard Summary":
    st.title("📈 Smart Dashboard Overview")
    city_options = ["Sustainoville", "EcoCity", "Greenopolis"]
    city = st.selectbox("🏩 Select your Smart City", city_options)
    st.markdown(f"### 🧽 Real-time Overview for **{city}**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-label">Water Usage (Litres)</div><div class="metric-value">1.2M</div><div class="metric-delta">▼ 2.3%</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-label">Energy Consumption (kWh)</div><div class="metric-value">4.7M</div><div class="metric-delta">▲ 1.1%</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-label">Air Quality Index</div><div class="metric-value">67</div><div class="metric-delta">▼ 5</div></div>', unsafe_allow_html=True)
    st.subheader("🌿 Sustainability Tips")
    st.markdown("- 💧 Implement rainwater harvesting systems\n- ⚡ Use motion sensors\n- 🌿 Expand green zones")

elif selected == "🍃 Eco Tips":
    st.title("🌱 Eco Tips Generator")
    topic = st.text_input("Enter a topic (e.g. water, waste, traffic)")
    if st.button("Get Eco Tip"):
        r = requests.post(f"{BASE_URL}/get-eco-tip", json={"topic": topic})
        st.success(r.json().get("tip"))

elif selected == "📊 KPI Forecasting":
    st.title("📊 KPI Forecasting")
    file = st.file_uploader("📂 Upload KPI .csv file", type="csv")

    if file:
        if st.button("📈 Predict KPI"):
            try:
                r = requests.post(f"{BASE_URL}/upload-kpi", files={"file": file})
                if r.status_code == 200:
                    try:
                        result = r.json()
                        forecast = result.get("forecast", {})
                        next_year = forecast.get("next_year")
                        prediction = forecast.get("predicted_value")
                        st.write("🧪 Debug:", next_year, prediction)

                        if next_year and prediction:
                            st.markdown("### 🔍 KPI Forecast Summary")
                            st.markdown(f"""
                                <div style='
                                    display: flex;
                                    flex-direction: row;
                                    gap: 2rem;
                                    margin-top: 10px;
                                '>
                                    <div style='
                                        flex: 1;
                                        background-color:#f3f8ff;
                                        padding: 20px;
                                        border-radius: 12px;
                                        box-shadow: 2px 2px 10px rgba(0,0,0,0.08);
                                        text-align: center;
                                    '>
                                        <h5>📅 Predicted Year</h5>
                                        <p style='font-size: 28px; color: #1565c0; font-weight: bold;'>{next_year}</p>
                                    </div>
                                    <div style='
                                        flex: 1;
                                        background-color:#f3f8ff;
                                        padding: 20px;
                                        border-radius: 12px;
                                        box-shadow: 2px 2px 10px rgba(0,0,0,0.08);
                                        text-align: center;
                                    '>
                                        <h5>📈 KPI</h5>
                                        <p style='font-size: 28px; color: #2e7d32; font-weight: bold;'>Energy Consumption</p>
                                    </div>
                                    <div style='
                                        flex: 1;
                                        background-color:#f3f8ff;
                                        padding: 20px;
                                        border-radius: 12px;
                                        box-shadow: 2px 2px 10px rgba(0,0,0,0.08);
                                        text-align: center;
                                    '>
                                        <h5>📊 Predicted Value</h5>
                                        <p style='font-size: 28px; color: #d84315; font-weight: bold;'>{prediction} kWh</p>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

                            # Highlighted callout box
                            st.markdown(f"""
                                <div style='
                                    background-color: #fff3e0;
                                    padding: 25px;
                                    border-left: 6px solid #ff6f00;
                                    margin-top: 25px;
                                    border-radius: 10px;
                                    font-size: 20px;
                                    font-weight: 600;
                                    color: #bf360c;
                                    box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
                                '>
                                    🎯 Forecasted Energy for <strong>{next_year}</strong> is <strong>{prediction} kWh</strong>
                                </div>
                            """, unsafe_allow_html=True)

                            # Chart
                            df = pd.DataFrame({
                                "Year": forecast.get("input_years", []) + [next_year],
                                "Energy": forecast.get("input_values", []) + [prediction]
                            })

                            st.markdown("### 📉 Forecast Trend")
                            st.line_chart(df.set_index("Year"))
                        else:
                            st.warning("⚠️ Forecast result is missing.")
                    except Exception:
                        st.error("❌ Invalid JSON response from server.")
                        st.text(r.text)
                else:
                    st.error(f"❌ API returned {r.status_code}")
                    st.text(r.text)
            except Exception as e:
                st.error(f"🔥 Request error: {e}")

elif selected == "🔍 Anomaly Detection":
    st.markdown("<h2 style='color:#c62828;'>🚨 Anomaly Detection</h2>", unsafe_allow_html=True)
    file = st.file_uploader("📄 Upload .csv file", type="csv")
    kpi = st.text_input("🔢 Enter KPI column name")
    threshold = st.number_input("⚙️ Threshold", value=1000.0)

    if file and st.button("🔍 Detect"):
        response = requests.post(
            f"{BASE_URL}/check-anomalies",
            files={"file": file},
            data={"kpi": kpi, "threshold": threshold}
        )
        if response.status_code == 200:
            result = response.json()
            anomalies = result.get("anomalies", [])
            st.success(f"✅ Found {len(anomalies)} anomaly points")
            if anomalies:
                df = pd.DataFrame(anomalies, columns=["Year", "Energy Consumption"])
                st.markdown("### 🚨 Anomalies Detected")
                st.dataframe(df)
                st.markdown("### 📈 Anomaly Chart")
                fig, ax = plt.subplots()
                ax.plot(df["Year"], df["Energy Consumption"], marker='o', color='orange', label='Anomalies')
                ax.axhline(y=threshold, color='red', linestyle='--', label='Threshold')
                ax.set_xlabel("Year")
                ax.set_ylabel("Energy Consumption")
                ax.set_title("Energy Anomalies by Year")
                ax.legend()
                st.pyplot(fig)
            else:
                st.info("No anomalies detected in the uploaded file.")
        else:
            st.error(f"❌ Server error: {response.status_code}")
            st.text(response.text)

elif selected == "📘 Sustainability Report":
    st.title("📘 Sustainability Report Generator")

    option = st.radio("Choose input method", ["Enter Text", "Upload .txt File"])

    if option == "Enter Text":
        content = st.text_area("Paste your KPI data or sustainability metrics here:")
        if st.button("Generate Report"):
            r = requests.post(f"{BASE_URL}/generate-report", json={"text": content})
            report = r.json().get("report")
            if report:
                st.markdown(report)
                st.download_button("📄 Download Markdown", report, file_name="report.md")
                pdf_path = convert_to_pdf(report)
                with open(pdf_path, "rb") as f:
                    st.download_button("📄 Download PDF", f, file_name="report.pdf")
            else:
                st.warning("⚠️ No report returned from backend.")

    else:
        uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
        if uploaded_file and st.button("Generate from File"):
            content = uploaded_file.read().decode("utf-8")
            r = requests.post(f"{BASE_URL}/upload-txt-generate-pdf", files={"file": ("file.txt", content)})
            result = r.json()
            report = result.get("summary")
            if report:
                st.markdown(report)
                st.download_button("📄 Download Markdown", report, file_name="report.md")
                pdf_url = result.get("pdf_path")
                with open(pdf_url, "rb") as f:
                    st.download_button("📄 Download PDF", f, file_name="report.pdf")
            else:
                st.warning("⚠️ No report generated.")


elif selected == "📄 Policy Summarizer":
    st.title("📄 Policy Summarizer")

    method = st.radio("Choose input method", ["Paste Text", "Upload .txt File"])

    if method == "Paste Text":
        input_text = st.text_area("Paste policy text", height=300)
        if st.button("Generate Summary"):
            if input_text.strip():
                res = requests.post(
                    f"{BASE_URL}/policy/summarize-policy",
                    json={"text": input_text}
                )
                summary = res.json().get("summary")
                if summary:
                    st.success("✅ Summary Generated")
                    st.markdown(summary)
                else:
                    st.warning("⚠️ No summary returned from backend.")
            else:
                st.warning("⚠️ Please enter policy text.")

    else:
        uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
        if uploaded_file and st.button("Generate Summary from File"):
            # read the file and send it to backend
            res = requests.post(
                f"{BASE_URL}/policy/summarize-uploaded-file",
                files={"file": (uploaded_file.name, uploaded_file, "text/plain")}
            )
            print("Status:", res.status_code)
            print("Response Text:", res.text)
            summary = res.json().get("summary")
            if summary:
                st.success("✅ Summary Generated")
                st.markdown(summary)
            else:
                st.warning("⚠️ No summary returned from backend.")


elif selected == "🤖 Chat Assistant":
    st.title("💬 Chat with Assistant")
    doc = st.file_uploader("Optional: Upload context file", type="txt")
    question = st.text_area("Your question")
    if st.button("Ask"):
        context = doc.read().decode("utf-8") if doc else ""
        full_prompt = f"{context}\n\n{question}" if context else question
        r = requests.post(f"{BASE_URL}/chat/ask", json={"prompt": full_prompt})
        st.write(r.json().get("response"))

elif selected == "📋 Citizen Feedback":
    st.title("📋 Citizen Feedback Log")
    try:
        import json
        with open("app/data/feedback_log.json", "r") as f:
            feedback_data = json.load(f)
        df = pd.DataFrame(feedback_data)
        st.dataframe(df)
    except Exception as e:
        st.error("❌ Could not load feedback log.")
        st.text(str(e))
