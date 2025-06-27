from fastapi import APIRouter

router = APIRouter()

@router.get("/pinecone-status", tags=["Pinecone"])
def check_pinecone():
    return {"pinecone": "Connected (placeholder response)"}
