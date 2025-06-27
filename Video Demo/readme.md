# 🌆 Smart City Assistant

A real-time AI-powered assistant that empowers cities to become smarter, greener, and more responsive.  
This project integrates **AI-driven analytics**, **policy insights**, and **citizen engagement** into a single streamlined dashboard — built using **FastAPI**, **Streamlit**, and **IBM Watsonx**.

## 🎥 Demo Video  
🎬 Watch the full demo: [Smart City Assistant in Action]

---

## 🧭 What It Solves

Managing urban sustainability is complex. This assistant simplifies it by:

- Turning **raw KPIs** into actionable forecasts  
- Automatically **summarizing policy documents** for better understanding  
- Detecting **anomalies in environmental trends**  
- Offering **eco-friendly suggestions** tailored to specific city needs  
- Generating professional **PDF/Markdown sustainability reports**  
- Allowing real-time **Q&A with an AI model trained on city metrics**  
- Logging and displaying **citizen feedback** for transparency

---

## ⚙️ How It Works

1. **Frontend (Streamlit)** – clean, interactive dashboard for users  
2. **Backend (FastAPI)** – handles file processing, LLM calls, PDF generation  
3. **AI Integration (IBM Watsonx + LangChain)** – handles report generation, chat, summarization  
4. **Local storage** – saves all reports and logs under `app/data/`

---

## 📦 Project Setup

1. Set up `.env` with Watsonx credentials
2. Run backend:
   ```bash
   uvicorn main:app --reload
