import sys
import os

# Dynamically add Project_Files to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))  # this points to Project_Files/
sys.path.insert(0, project_root)  # make it highest priority

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

elif selected == "🌱 Eco Tips Generator":
    st.title("🌱 Eco Tips Generator")
    user_input = st.text_input("Enter a topic and number of tips (e.g. traffic 10)")

    if user_input:
        try:
            parts = user_input.strip().rsplit(" ", 1)
            topic = parts[0]
            count = int(parts[1]) if len(parts) == 2 and parts[1].isdigit() else 5
            r = requests.get(f"{BASE_URL}/eco/tips", params={"topic": topic, "count": count})

            if r.status_code == 200:
                tips = r.json().get("tips", [])
                if tips:
                    st.markdown("### 🌿 Eco Tips")
                    for i, tip in enumerate(tips, 1):
                        st.markdown(f"{i}. {tip}")
                else:
                    st.warning("No tips returned.")
            else:
                st.error(f"❌ Server returned status code {r.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")

elif selected == "🔍 Anomaly Detection":
    st.title("🚨 Anomaly Detection")
    file = st.file_uploader("📄 Upload .csv file", type="csv")
    kpi = st.text_input("🔢 Enter KPI column name (e.g., Energy Consumption)")
    threshold = st.number_input("⚙️ Threshold", value=1000.0)

    if file and kpi and st.button("Detect Anomalies"):
        try:
            response = requests.post(
                f"{BASE_URL}/anomaly/check-anomalies",
                files={"file": file},
                data={"kpi": kpi, "threshold": threshold}
            )
            if response.status_code == 200:
                result = response.json()
                anomalies = result.get("anomalies", [])

                if anomalies:
                    df = pd.DataFrame(anomalies)
                    st.success(f"✅ {len(df)} anomalies detected.")

                    st.markdown("### 🔍 Anomalies Table")
                    st.dataframe(df)

                    # Plot chart
                    st.markdown("### 📈 Anomaly Chart")
                    fig, ax = plt.subplots()
                    ax.plot(df.index, df[kpi], 'ro', label='Anomalies')
                    ax.axhline(y=threshold, color='blue', linestyle='--', label='Threshold')
                    ax.set_ylabel(kpi)
                    ax.set_title(f"Anomalies in {kpi}")
                    ax.legend()
                    st.pyplot(fig)
                else:
                    st.info("✅ No anomalies found based on the threshold.")
            else:
                st.error(f"❌ Server returned {response.status_code}")
                st.text(response.text)
        except Exception as e:
            st.error(f"🔥 Request failed: {e}")

elif selected == "📊 KPI Forecasting":
    st.title("📊 KPI Forecasting")
    file = st.file_uploader("📂 Upload KPI .csv file", type="csv")

    if file:
        if st.button("📈 Predict KPI"):
            try:
                r = requests.post(f"{BASE_URL}/kpi-upload/upload-kpi", files={"file": file})
                if r.status_code == 200:
                    result = r.json()
                    forecast = result.get("forecast", {})
                    next_year = forecast.get("next_year")
                    prediction = forecast.get("predicted_value")

                    st.markdown("### 🔍 KPI Forecast Summary")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("📅 Year", next_year)
                    col2.metric("📈 KPI", "Energy Consumption")
                    col3.metric("🔮 Predicted", f"{prediction} kWh")

                    df = pd.DataFrame({
                        "Year": forecast.get("input_years", []) + [next_year],
                        "Energy": forecast.get("input_values", []) + [prediction]
                    })

                    st.markdown("### 📉 Forecast Trend")
                    st.line_chart(df.set_index("Year"))
                else:
                    st.error(f"❌ Error: {r.status_code}")
                    st.text(r.text)
            except Exception as e:
                st.error(f"🔥 Request failed: {e}")


elif selected == "📘 Sustainability Report":
    st.title("📘 Sustainability Report Generator")

    option = st.radio("Choose input method", ["Enter Text", "Upload .txt File"])

    if option == "Enter Text":
        content = st.text_area("Paste your KPI data or sustainability metrics here:")
        if st.button("Generate Report"):
            try:
                # ✅ CORRECTED endpoint
                r = requests.post(f"{BASE_URL}/report/generate-report", json={"text": content})
                if r.status_code == 200:
                    report = r.json().get("report")
                    if report:
                        st.markdown("### 📝 Generated Report")
                        st.markdown(report)
                        st.download_button("📄 Download Markdown", report, file_name="report.md")

                        # Convert to PDF
                        pdf_path = convert_to_pdf(report)
                        with open(pdf_path, "rb") as f:
                            st.download_button("📄 Download PDF", f, file_name="report.pdf")
                    else:
                        st.warning("⚠️ No report returned from backend.")
                else:
                    st.error(f"❌ Error: {r.status_code}")
                    st.text(r.text)
            except Exception as e:
                st.error(f"🔥 Request failed: {e}")

    else:
        uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
        if uploaded_file and st.button("Generate from File"):
            try:
                content = uploaded_file.read().decode("utf-8")
                # ✅ CORRECTED endpoint
                r = requests.post(f"{BASE_URL}/report/upload-txt-generate-pdf", files={"file": ("file.txt", content)})

                if r.status_code == 200:
                    result = r.json()
                    report = result.get("summary")
                    pdf_path = result.get("pdf_path")
                    if report:
                        st.markdown("### 📝 Generated Report")
                        st.markdown(report)
                        st.download_button("📄 Download Markdown", report, file_name="report.md")
                        with open(pdf_path, "rb") as f:
                            st.download_button("📄 Download PDF", f, file_name="report.pdf")
                    else:
                        st.warning("⚠️ No report returned.")
                else:
                    st.error(f"❌ Error: {r.status_code}")
                    st.text(r.text)
            except Exception as e:
                st.error(f"🔥 Upload failed: {e}")


elif selected == "📄 Policy Summarizer":
    st.title("📄 Policy Summarizer")

    method = st.radio("Choose input method", ["Paste Text", "Upload .txt File"])

    if method == "Paste Text":
        input_text = st.text_area("Paste policy text", height=300)
        if st.button("Generate Summary"):
            if input_text.strip():
                try:
                    res = requests.post(
                        f"{BASE_URL}/policy/policy/summarize-policy",  # ✅ Correct endpoint
                        json={"text": input_text}
                    )
                    if res.status_code == 200:
                        summary = res.json().get("summary")
                        if summary:
                            st.success("✅ Summary Generated")
                            st.markdown(summary)
                        else:
                            st.warning("⚠️ No summary returned from backend.")
                    else:
                        st.error(f"❌ API Error: {res.status_code}")
                        st.text(res.text)
                except Exception as e:
                    st.error(f"🔥 Request failed: {e}")
            else:
                st.warning("⚠️ Please enter policy text.")

    else:
        uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
        if uploaded_file and st.button("Generate Summary from File"):
            try:
                file_bytes = uploaded_file.read()
                res = requests.post(
                    f"{BASE_URL}/policy/policy/summarize-uploaded-file",  # ✅ Correct endpoint
                    files={"file": (uploaded_file.name, file_bytes, "text/plain")}
                )
                if res.status_code == 200:
                    summary = res.json().get("summary")
                    if summary:
                        st.success("✅ Summary Generated")
                        st.markdown(summary)
                    else:
                        st.warning("⚠️ No summary returned from backend.")
                else:
                    st.error(f"❌ API Error: {res.status_code}")
                    st.text(res.text)
            except Exception as e:
                st.error(f"🔥 Upload failed: {e}")


elif selected == "🤖 Chat Assistant":
    st.title("💬 Chat with Assistant")
    doc = st.file_uploader("Optional: Upload context file", type="txt")
    question = st.text_area("Your question")
    if st.button("Ask"):
        context = doc.read().decode("utf-8") if doc else ""
        full_prompt = f"{context}\n\n{question}" if context else question
        r = requests.post(f"{BASE_URL}/chat/ask", json={"prompt": full_prompt})
        st.write(r.json().get("response"))

elif selected == "📋 Citizen Feedback Log":
    st.title("📋 Citizen Feedback Log")
    try:
        r = requests.get(f"{BASE_URL}/feedback/list")
        if r.status_code == 200:
            feedbacks = r.json().get("feedback", [])
            if feedbacks:
                for fb in feedbacks:
                    st.markdown(f"**🧑 {fb['name']}**: {fb['feedback']}")
            else:
                st.warning("No feedback found.")
        else:
            st.error(f"Could not load feedback: {r.status_code}")
    except Exception as e:
        st.error(f"🔥 Error: {e}")

