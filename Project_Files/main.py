from dotenv import load_dotenv
load_dotenv(override=True)


from fastapi import FastAPI
from app.api import api_router  # or wherever your routes are
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Watsonx LLM function for legacy direct call
from app.services.granite_llm import ask_granite

# Create FastAPI app instance first
app = FastAPI()
app.include_router(api_router)  # if you use a router

# Setup CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and register routers
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

# Register routers
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

# Optional legacy endpoint to test direct Watsonx LLM
class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask-assistant/")
def ask_city_assistant(request: PromptRequest):
    response = ask_granite(request.prompt)
    return {"response": response}

@app.get("/")
def read_root():
    return {"message": "Smart City Assistant is running!"}

