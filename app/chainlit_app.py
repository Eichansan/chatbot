import chainlit as cl
from config import Config
import httpx

# チャットが開始されたときに実行される関数
@cl.on_chat_start 
async def on_chat_start():
    await cl.Message(content="The application has been activated! Please enter your message!").send() # 初期表示されるメッセージを送信する

# メッセージが送信されたときに実行される関数
@cl.on_message 
async def on_message(input_message):
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:  # タイムアウトを10秒に設定
        try:
            response = await client.post(
                Config.FASTAPI_URL + "/chat",
                json={"question": input_message.content}  # FastAPI のエンドポイントにリクエストを送信
            )

            data = response.json()  # 非同期でJSONを取得
            answer = data.get("response", "No response received.")
        
        except httpx.HTTPStatusError as e:
            answer = f"HTTP Error: {e.response.status_code} - {e.response.text}"
        except httpx.TimeoutException:
            answer = "The request timed out. Please try again later."
        except Exception as e:
            answer = f"Error: {str(e)}"
    
    await cl.Message(content=answer).send() # チャットボットからの返答を送信する