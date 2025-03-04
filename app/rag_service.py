from openai import AsyncOpenAI
from .vector_store import search_similar_documents
from .config import config

api_key = config.OPENAI_API_KEY

async def handle_query(query):
    docs = search_similar_documents(query)
    context = "\n".join([doc['content'] for doc in docs])

    system_prompt = "以下は研究室のPukiWikiに保存された情報です。以下の情報を参考にして質問に答えてください。\n\n" + context

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    async for chunk in client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True
    ):
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
