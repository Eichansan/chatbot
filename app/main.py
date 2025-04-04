from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from ai_message import generate_response
from rag_service import rag_search

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/chat")
async def generate_answer(request: QuestionRequest) -> Dict[str, Any]:
    question = request.question
    prompt = rag_search(question)

    if prompt is None:
        raise HTTPException(status_code=404, detail="適切な回答が見つかりませんでした。")

    response = generate_response(prompt)
    return {"question": question, "response": response}
