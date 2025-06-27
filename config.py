from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    watsonx_api_key: str = os.getenv("WATSONX_API_KEY")
    watsonx_project_id: str = os.getenv("WATSONX_PROJECT_ID")
    watsonx_url: str = os.getenv("WATSONX_URL")
    watsonx_model_id: str = os.getenv("WATSONX_MODEL_ID")

    pinecone_api_key: str = os.getenv("PINECONE_API_KEY")
    pinecone_env: str = os.getenv("PINECONE_ENV")
    index_name: str = os.getenv("INDEX_NAME")

settings = Settings()
