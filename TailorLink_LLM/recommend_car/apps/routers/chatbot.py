import random
import time
import hashlib
import asyncio
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from recommend_car.apps.db import SessionLocal, get_car_info_from_db
from recommend_car.apps.prompt_manager import get_system_prompt
from recommend_car.apps.utils import (
    get_openai_response,
    create_empty_faiss_index,
    search_faiss,
    get_documents_by_indices,
    update_faiss_with_external_data,
    embeddings
)

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

class ChatResponse(BaseModel):
    response: str = Field(...)
    session_id: str = Field(...)
    history: List[Message] = Field(...)
    car_id: str = Field(...)

# SHA256 해싱으로 고유한 세션 ID 생성
def generate_session_id() -> str:
    while True:
        random_number = random.randint(1000000000, 9999999999)
        session_id = hashlib.sha256(str(random_number).encode()).hexdigest()[:16]
        if session_id not in conversation_memory:
            return session_id

# 사용되지 않은 세션 삭제
def cleanup_sessions():
    current_time = time.time()
    expired_sessions = [
        session_id
        for session_id, session_data in conversation_memory.items()
        if (current_time - session_data["last_access"]) > SESSION_EXPIRY_SECONDS
    ]
    for session_id in expired_sessions:
        del conversation_memory[session_id]

# 세션별 데이터 관리
def initialize_session(session_id):
    if session_id not in conversation_memory:
        # 세션 초기화
        conversation_memory[session_id] = {
            "last_access": time.time(),
            "history": [],
            "system_message": {
                "role": "system",
                "content": get_system_prompt()
            },
            "documents": [],
            "faiss_index": create_empty_faiss_index(len(embeddings.embed_query("샘플")))
        }

@router.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest, db: Session = Depends(get_db)):
    # 세션 ID 생성 또는 가져오기
    session_id = chat_request.session_id or generate_session_id()
    user_input = chat_request.user_input

    # 세션 초기화
    initialize_session(session_id)

    # 세션 데이터 가져오기
    session_data = conversation_memory[session_id]
    session_data["last_access"] = time.time()
    conversation_history = session_data["history"]
    documents = session_data["documents"]
    faiss_index = session_data["faiss_index"]

    # 사용자 입력 추가
    conversation_history.append({"role": "user", "content": user_input})

    # DB에서 차량 정보 검색
    car_info = get_car_info_from_db(db, user_input)
    if car_info:
        # DB에서 차량 정보를 찾은 경우
        context = f"{car_info.name}에 대한 정보입니다: {car_info.description}"
    else:
        # 비동기적으로 외부 데이터 업데이트
        asyncio.create_task(update_faiss_with_external_data(faiss_index, user_input, documents))

        # 현재 FAISS 인덱스에서 검색
        search_indices = search_faiss(faiss_index, user_input, k=3)
        search_results = get_documents_by_indices(documents, search_indices)
        context = "\n".join(search_results)

    # 모델에게 전달할 메시지 구성
    assistant_prompt = get_system_prompt()
    openai_history = [session_data["system_message"]] + conversation_history

    # OpenAI API 호출
    try:
        ai_response = get_openai_response(openai_history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API 호출 중 오류 발생: {str(e)}")

    # 응답 추가
    conversation_history.append({"role": "assistant", "content": ai_response})
    cleanup_sessions()
    return ChatResponse(
        response=ai_response,
        session_id=session_id,
        history=conversation_history
    )   
