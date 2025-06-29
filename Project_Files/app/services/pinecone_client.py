import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

# Load credentials
api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENVIRONMENT")  # ✅ Match Render Secret
index_name = os.getenv("PINECONE_INDEX_NAME")    # ✅ Match Render Secret

# Initialize Pinecone client
pc = Pinecone(api_key=api_key)

# Create index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region=environment
        )
    )

# Get index object
index = pc.Index(index_name)

