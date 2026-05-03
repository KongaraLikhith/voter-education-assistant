from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from services.gemini_service import get_gemini_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

@router.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = await get_gemini_response(request.message, request.history)
        return {"response": response, "success": True}
    except Exception as e:
        return {"response": f"An error occurred: {str(e)}", "success": False}
