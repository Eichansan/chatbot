from config import Config
import ollama
import re
import qdrant_client
from qdrant_client.models import PointStruct, Distance, VectorParams

# Qdrant クライアントの初期化
qdrant = qdrant_client.QdrantClient(Config.QDRANT_HOST, port=Config.QDRANT_PORT)

# コレクションを作成（既存の場合は削除して作り直す）
qdrant.recreate_collection(
    collection_name=Config.QDRANT_COLLECTION,
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)


def vectorize_text(text):
    """テキストをベクトル化"""
    response = ollama.embeddings(
        model=Config.OLLAMA_EMBEDDINGS_MODEL,
        prompt=text
    )
    return response["embedding"]


def load_text_file(filepath):
    """テキストファイルをロードしてセクションごとに分割"""
    with open(filepath, 'r', encoding='euc_jp') as file:
        content = file.read()
    sections = re.split(r'\n\s*(\*+.*?)\s*\n', content)
    chunks = []
    current_chunk = ""
    for section in sections:
        if section.startswith("*"):
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = section + "\n"
        else:
            current_chunk += section + "\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


# FAQ データをロード
answers = load_text_file('./wiki/example.txt')

# Qdrant にデータを保存
points = []
for i, answer in enumerate(answers):
    vector = vectorize_text(answer)
    point = PointStruct(id=i, vector=vector, payload={"text": answer})
    points.append(point)

qdrant.upsert(collection_name=Config.QDRANT_COLLECTION, points=points)

print(f"Qdrant に {len(answers)} 件のデータを保存完了！")
