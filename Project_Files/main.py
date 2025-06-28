import os
import sys
from dotenv import load_dotenv

# ✅ Ensure 'app/' is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, "app")
sys.path.append(app_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ✅ Correct imports after fixing path
from api import api_router
from api.chat_router import router as chat_router
from api.policy_router import router as policy_router
from api.feedback_router import router as feedback_router
from api.eco_tips_router import router as eco_tips_router
from api.report_router import router as report_router
from api.kpi_router import router as kpi_router
from api.kpi_upload_router import router as kpi_upload_router
from api.dashboard_router import router as dashboard_router
from api.vector_router import router as vector_router
from api.pinecone_router import router as pinecone_router
from api.anomaly_router import router as anomaly_router

from services.granite_llm import ask_granite  # ✅ should now work

# 🌍 Load .env
load_dotenv(override=True)

app = FastAPI(title="Smart City Assistant API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(api_router)
app.include_router(chat_router, prefix="/chat", tags=["Chat Assistant"])
app.include_router(policy_router, tags=["Policy Summarizer"])
app.include_router(feedback_router)
app.include_router(eco_tips_router)
app.include_router(report_router)
app.include_router(kpi_router)
app.include_router(kpi_upload_router)
app.include_router(dashboard_router)
app.include_router(vector_router)
app.include_router(pinecone_router)
app.include_router(anomaly_router)

# Watsonx test endpoint
class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask-assistant/")
def ask_city_assistant(request: PromptRequest):
    response = ask_granite(request.prompt)
    return {"response": response}

@app.get("/")
def root():
    return {"message": "Smart City Assistant is running!"}
