from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from config import Config
import ollama
from rag_service import rag_search

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

def generate_response(prompt, model=Config.OLLAMA_LLM):
    try:
        stream = ollama.generate(
            model=model,
            prompt=prompt,
            stream=True
        )
        
        response = ""
        for chunk in stream:
            response += chunk['response']
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def generate_answer(request: QuestionRequest) -> Dict[str, Any]:
    question = request.question
    prompt = rag_search(question)

    if prompt is None:
        raise HTTPException(status_code=404, detail="適切な回答が見つかりませんでした。")

    response = generate_response(prompt)
    return {"question": question, "response": response}
