from fastapi import APIRouter
from pydantic import BaseModel
from ..services.granite_llm import generate_eco_tip

router = APIRouter()

class TopicRequest(BaseModel):
    topic: str

@router.post("/get-eco-tip", tags=["Eco Tips"])
def get_eco_tip(data: TopicRequest):
    tip = generate_eco_tip(data.topic)
    return {"tip": tip}
