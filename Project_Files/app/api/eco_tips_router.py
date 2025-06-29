from fastapi import APIRouter, Query
from app.services.granite_llm import generate_eco_tip

router = APIRouter()

@router.get("/tips", tags=["Eco Tips"])
async def get_eco_tips(topic: str = Query(...), count: int = Query(5)):
    try:
        prompt = f"Give {count} practical, eco-friendly tips related to: {topic}. Use bullet points."
        response = generate_eco_tip(prompt)
        tips = response.strip().split("\n")
        tips = [tip.strip("-• ").strip() for tip in tips if tip.strip()]
        return {"tips": tips}
    except Exception as e:
        return {"error": str(e)}
