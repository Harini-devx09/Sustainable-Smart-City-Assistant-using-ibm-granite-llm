import json
import os
from fastapi import APIRouter

router = APIRouter()

@router.get("/list", tags=["Feedback"])
def get_feedback_log():
    filepath = "app/data/feedback_log.json"
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            feedbacks = json.load(f)
        return {"feedback": feedbacks}
    else:
        return {"feedback": []}
