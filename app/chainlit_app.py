import chainlit as cl
from fastapi import HTTPException

from ai_message import generate_response
from rag_service import rag_search
# チャットが開始されたときに実行される関数
@cl.on_chat_start 
async def on_chat_start():
    await cl.Message(content="The application has been activated! Please enter your message!").send() # 初期表示されるメッセージを送信する

# メッセージが送信されたときに実行される関数
@cl.on_message 
async def on_message(input_message: cl.Message):
    prompt = rag_search(input_message.content)
    if prompt is None:
        raise HTTPException(status_code=404, detail="適切な回答が見つかりませんでした。")

    msg = cl.Message(content="")

    stream = generate_response(prompt)
    
    async for token in stream:
        if token:
            await msg.stream_token(token)

    await msg.update()