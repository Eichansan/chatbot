import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FASTAPI_URL = os.getenv("FASTAPI_URL")
    
    QDRANT_HOST = os.getenv("QDRANT_HOST")
    QDRANT_PORT = os.getenv("QDRANT_PORT")
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")

    OLLAMA_EMBEDDINGS_MODEL = os.getenv("OLLAMA_EMBEDDINGS_MODEL")
    OLLAMA_LLM = os.getenv("OLLAMA_LLM")
config = Config()
