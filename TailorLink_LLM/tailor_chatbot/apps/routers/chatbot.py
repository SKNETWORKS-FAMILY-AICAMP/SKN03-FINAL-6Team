from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from apps.utils import get_openai_response

router = APIRouter()

# 요청 바디 모델 정의
class UserInput(BaseModel):
    user_input: str

@router.post("/chat")
async def chat_with_bot(user_input: UserInput):
    try:
        bot_response = get_openai_response(user_input.user_input)
        return {"user_input": user_input.user_input, "response": bot_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"요청 처리 중 에러 발생: {str(e)}")
