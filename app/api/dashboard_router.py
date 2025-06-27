from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard", tags=["Dashboard"])
def get_dashboard_data():
    return {
        "status": "online",
        "modules": [
            "chat assistant", "eco tips", "policy summarizer", "KPI prediction", "report generator"
        ]
    }
