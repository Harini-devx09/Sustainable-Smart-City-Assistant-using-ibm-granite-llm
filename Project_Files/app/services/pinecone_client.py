import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

# Load credentials
api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENV")  # E.g., 'us-west-1' or 'gcp-starter'
index_name = os.getenv("INDEX_NAME")

# Initialize Pinecone client
pc = Pinecone(api_key=api_key)

# Create index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",  # or 'dotproduct' or 'euclidean'
        spec=ServerlessSpec(
            cloud="aws",        # or "gcp"
            region=environment  # example: "us-west-2"
        )
    )

# Get index object for future use
index = pc.Index(index_name)
