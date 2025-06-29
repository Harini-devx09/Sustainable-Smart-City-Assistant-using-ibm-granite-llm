import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# ✅ Granite Watsonx import

# ✅ All routers
from app.api.chat_router import router as chat_router
from app.api.policy_router import router as policy_router
from app.api.feedback_router import router as feedback_router
from app.api.eco_tips_router import router as eco_tips_router
from app.api.report_router import router as report_router
from app.api.kpi_router import router as kpi_router
from app.api.kpi_upload_router import router as kpi_upload_router
from app.api.dashboard_router import router as dashboard_router
from app.api.vector_router import router as vector_router
from app.api.pinecone_router import router as pinecone_router
from app.api.anomaly_router import router as anomaly_router

# ✅ Granite Watsonx import
from app.services.granite_llm import ask_granite

app = FastAPI()

# ✅ CORS middleware: fixed to avoid browser issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # ← You can restrict this in production
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False     # ← Required when allow_origins=["*"]
)

# ✅ All routes
app.include_router(chat_router, prefix="/chat")
app.include_router(policy_router, prefix="/policy")
app.include_router(feedback_router, prefix="/feedback")
app.include_router(eco_tips_router, prefix="/eco")
app.include_router(report_router, prefix="/report")
app.include_router(kpi_router, prefix="/kpi")
app.include_router(kpi_upload_router, prefix="/kpi-upload")
app.include_router(dashboard_router, prefix="/dashboard")
app.include_router(vector_router, prefix="/vector")
app.include_router(pinecone_router, prefix="/pinecone")
app.include_router(anomaly_router, prefix="/anomaly")

# ✅ Watsonx test endpoint
class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask-assistant/")
def ask_city_assistant(request: PromptRequest):
    response = ask_granite(request.prompt)
    return {"response": response}

@app.get("/")
def root():
    return {"message": "Smart City Assistant is running!"}
