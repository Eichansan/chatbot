import os
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models
from config import config

api_key = config.OPENAI_API_KEY

client = OpenAI(api_key=api_key)
qdrant = QdrantClient("qdrant", port=6333)  # Docker内で動くQdrant

qdrant.recreate_collection(
    collection_name="pukiwiki_pages",
    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)
)

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def insert_page(title, content):
    embedding = get_embedding(content)
    qdrant.upsert(
        collection_name="pukiwiki_pages",
        points=[
            models.PointStruct(
                id=title,
                vector=embedding,
                payload={"title": title, "content": content}
            )
        ]
    )

def load_pukiwiki_data():
    wiki_dir = config.PUKIWIKI_DATA_DIR
    for filename in os.listdir(wiki_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(wiki_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                title = os.path.splitext(filename)[0]
                insert_page(title, content)
            print(f"Registered: {title}")

if __name__ == "__main__":
    load_pukiwiki_data()
