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

def generate_response(prompt, model="phi3:3.8b-mini-4k-instruct-q5_K_M"):
    try:
        stream = ollama.generate(
            model=model,
            prompt=prompt,
            stream=True
        )
        
        response = ""
        for chunk in stream:
            c = chunk['response']
            print(c, end='', flush=True)
            response += c
        
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    question1 = "VPN接続の方法は？"
    print(f"質問: {question1}")
    prompt = rag_search(question1)
    print(f"プロンプト: {prompt}")
    response = generate_response(prompt)
    print(f"\n回答: {response}")
