from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chat_assistant import ask_city_assistant

router = APIRouter()

class ChatPrompt(BaseModel):
    prompt: str

@router.post("/ask", tags=["Chat Assistant"])
def chat_with_city_assistant(data: ChatPrompt):
    response = ask_city_assistant(data.prompt)
    return {"response": response}
