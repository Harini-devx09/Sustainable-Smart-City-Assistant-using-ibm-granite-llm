from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chat_assistant import ask_city_assistant

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str

@router.post("/ask")
def chat_with_city_assistant(request: ChatRequest):
    response = ask_city_assistant(request.prompt)
    return {"response": response}
