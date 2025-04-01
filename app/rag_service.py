from config import Config
import ollama
import qdrant_client

qdrant = qdrant_client.QdrantClient(Config.QDRANT_HOST, port=Config.QDRANT_PORT)

def vectorize_text(text):
    """テキストをベクトル化"""
    response = ollama.embeddings(
        model=Config.OLLAMA_EMBEDDINGS_MODEL,
        prompt=text
    )
    return response["embedding"]

def rag_search(question):
    """質問に最も関連する回答を取得"""
    # 質問をベクトル化
    question_vector = vectorize_text(question)

    # Qdrant で検索
    results = qdrant.search(
        collection_name=Config.QDRANT_COLLECTION,
        query_vector=question_vector,
        limit=3
    )
    print(f"検索結果: {results}")

    if results:
        context = "\n\n".join([f"{i+1}. {hit.payload['text']}" for i, hit in enumerate(results)])
        # TODO プロンプトの内容を調整
        prompt = f"""
        次の質問について、3つの情報を基に簡潔に回答して下さい。
        # 質問
        {question}

        # 情報
        {context}
            
        # 回答
        """
        return prompt
    else:
        return "適切な回答が見つかりませんでした。"