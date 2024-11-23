# app/routers/chat.py
from fastapi import APIRouter
from app.models import ChatRequest
from app.helpers import generate_bot_response

router = APIRouter()

@router.post("/chat/")
async def chat(request: ChatRequest):
    user_input = request.user_input
    bot_response = generate_bot_response(user_input)
    return {"bot_response": bot_response}
