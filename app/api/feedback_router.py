from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Feedback(BaseModel):
    name: str
    category: str
    message: str

@router.post("/feedback", tags=["Citizen Feedback"])
def submit_feedback(feedback: Feedback):
    print("Feedback received:", feedback)
    return {"status": "success", "feedback": feedback}
