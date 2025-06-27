from sentence_transformers import SentenceTransformer
from app.services.pinecone_client import index

# Use the same model as embedding
retriever_model = SentenceTransformer("all-MiniLM-L6-v2")

def search_policy(query: str, top_k: int = 3):
    query_vector = retriever_model.encode(query).tolist()

    search_result = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )

    matches = [
        match["metadata"]["text"]
        for match in search_result.get("matches", [])
    ]

    return {"matches": matches}
