from fastapi import APIRouter
from pydantic import BaseModel
from app.services.document_embedder import embed_and_store
from app.services.document_retriever import search_policy
from fastapi import UploadFile, File

router = APIRouter()

class SearchQuery(BaseModel):
    query: str

@router.post("/upload-policy", tags=["Vector Store"])
async def upload_policy_document(file: UploadFile = File(...)):
    text = (await file.read()).decode("utf-8")
    result = embed_and_store(text, metadata={"filename": file.filename})
    return result

@router.post("/search-policy", tags=["Vector Store"])
def search_policy_endpoint(query: SearchQuery):
    results = search_policy(query.query)
    return results

