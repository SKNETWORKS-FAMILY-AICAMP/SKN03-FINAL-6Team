import random
import time
import hashlib
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from apps.utils import get_openai_response
from apps.db import SessionLocal, get_car_model_by_id

router = APIRouter()

# 메모리 저장소
conversation_memory = {}

# 세션 만료 시간 (1시간)
SESSION_EXPIRY_SECONDS = 3600

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Message(BaseModel):
    role: str = Field(...)
    content: str = Field(...)


class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(None)
    user_input: str = Field(...)
    model_id: Optional[int] = Field(None)

class CarInfo(BaseModel):
    name: str
    description: str
    image_url: str

class ChatResponse(BaseModel):
    response: str = Field(...)
    session_id: str = Field(...)
    history: List[Message] = Field(...)
    car_info: Optional[CarInfo] = None

# SHA256 해싱을 적용하여 고유한 16자리 세션 ID로 만들어 보안상의 단점을 보완
# 기존에는 랜덤 숫자로 부여하였음.
def generate_session_id() -> str:
    while True:
        random_number = random.randint(1000000000, 9999999999)
        session_id = hashlib.sha256(str(random_number).encode()).hexdigest()[:16]  
        if session_id not in conversation_memory:
            return session_id


#사용되지 않은 세션 삭제
def cleanup_sessions():
    current_time = time.time()
    expired_sessions = [
        session_id
        for session_id, session_data in conversation_memory.items()
        if (current_time - session_data["last_access"]) > SESSION_EXPIRY_SECONDS
    ]
    for session_id in expired_sessions:
        del conversation_memory[session_id]


@router.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    # 랜덤 숫자 기반 세션 ID 생성
    session_id = chat_request.session_id or generate_session_id()
    user_input = chat_request.user_input
    model_id = chat_request.model_id
    # 세션 초기화
    if session_id not in conversation_memory:
        conversation_memory[session_id] = {
            "last_access": time.time(),
            "history": []
        }

    # 세션 데이터 가져오기
    session_data = conversation_memory[session_id]
    session_data["last_access"] = time.time()  # 마지막 접근 시간 갱신
    conversation_history = session_data["history"]

    # 사용자 메시지 추가
    conversation_history.append(Message(role="user", content=user_input))

    try:
        ai_response = get_openai_response([msg.dict() for msg in conversation_history])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API 호출 중 오류 발생: {str(e)}")
    conversation_history.append(Message(role="assistant", content=ai_response))

    # 사용되지 않은 세션 정리
    cleanup_sessions()

    # 응답 반환
    return ChatResponse(
        response=ai_response,
        session_id=session_id,
        history=conversation_history
    )
