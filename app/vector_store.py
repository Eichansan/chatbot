from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI
from config import config

api_key = config.OPENAI_API_KEY
qdrant = QdrantClient("qdrant", port=6333)
client = OpenAI(api_key=api_key)

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def search_similar_documents(query):
    query_vector = get_embedding(query)
    search_result = qdrant.search(
        collection_name="pukiwiki_pages",
        query_vector=query_vector,
        limit=5
    )
    return [
        {"title": hit.payload["title"], "content": hit.payload["content"]}
        for hit in search_result
    ]
