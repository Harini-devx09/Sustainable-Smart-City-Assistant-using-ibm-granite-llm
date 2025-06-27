import uuid
from sentence_transformers import SentenceTransformer
from app.services.pinecone_client import index  # ✅ Use pinecone_client, not pinecone

embedder = SentenceTransformer('all-MiniLM-L6-v2')

def embed_and_store(document_text: str, metadata: dict = None):
    chunks = document_text.split("\n\n")
    vectors = embedder.encode(chunks).tolist()

    pinecone_vectors = []
    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        pinecone_vectors.append({
            "id": str(uuid.uuid4()),
            "values": vector,
            "metadata": {
                "text": chunk,
                **(metadata or {})
            }
        })

    index.upsert(vectors=pinecone_vectors)
    return {"status": "uploaded", "chunks": len(chunks)}
