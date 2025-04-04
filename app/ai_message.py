from fastapi import HTTPException
from config import Config
import ollama

async def generate_response(prompt, model=Config.OLLAMA_LLM):
    try:
        stream = ollama.generate(
            model=model,
            prompt=prompt,
            stream=True
        )
        
        for chunk in stream:
            yield chunk['response']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    