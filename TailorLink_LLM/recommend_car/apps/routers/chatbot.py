import random
import time
import hashlib
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from recommend_car.apps.db import SessionLocal, get_car_info_from_db
from recommend_car.apps.prompt_manager import get_system_prompt
from recommend_car.apps.utils import (
    get_openai_response, 
    create_faiss_index, 
    load_documents, 
    search_faiss, 
    get_documents_by_indices,
    is_car_recommendation,
    is_genesis
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

# 문서 로드 및 FAISS 인덱스 생성
documents = load_documents()
faiss_index = create_faiss_index(documents)

@router.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest, db: Session = Depends(get_db)):
    # 세션 ID 생성 또는 가져오기
    session_id = chat_request.session_id or generate_session_id()
    user_input = chat_request.user_input
    model_id = chat_request.model_id

    # 세션 초기화
    if session_id not in conversation_memory:
        conversation_memory[session_id] = { 
            "last_access": time.time(),
            "history": []  # 시스템 메시지는 별도로 관리
        }
        # 시스템 프롬프트 추가 (OpenAI API에만 사용)
        conversation_memory[session_id]["system_message"] = {
            "role": "system",
            "content": get_system_prompt()
        }

    # 세션 데이터 가져오기
    session_data = conversation_memory[session_id]
    session_data["last_access"] = time.time()  # 마지막 접근 시간 갱신
    conversation_history = session_data["history"]

    # 사용자 메시지 추가
    conversation_history.append({"role": "user", "content": user_input})

    # FAISS 검색 수행
    search_indices = search_faiss(faiss_index, user_input)
    search_results = get_documents_by_indices(documents, search_indices)

    # OpenAI 호출용 메시지 구성 (시스템 메시지 포함)
    openai_history = [session_data["system_message"]] + conversation_history

    # 차량 추천 내용인지 판단
    if is_car_recommendation(search_results):
        # 제네시스 차량 여부 판단
        if is_genesis(user_input):
            # DB에서 제네시스 차량 정보 조회
            car_info = get_car_info_from_db(db, user_input)
            if not car_info:
                # 해당 차량 정보가 없으면 에러 처리 또는 기본 응답
                ai_response = "죄송하지만 요청하신 제네시스 차량 정보를 찾을 수 없습니다."
            else:
                # OpenAI API 호출을 위한 프롬프트 구성
                assistant_prompt = f"다음 제네시스 차량을 추천합니다: {car_info.name}. {car_info.description}"
                conversation_history.append({"role": "assistant", "content": assistant_prompt})
                ai_response = assistant_prompt  # 실제로는 OpenAI API를 호출하여 응답 생성 가능
        else:
            recommended_cars = ', '.join(search_results)
            assistant_prompt = f"다음 차량을 추천합니다: {recommended_cars}"
            conversation_history.append({"role": "assistant", "content": assistant_prompt})
            ai_response = assistant_prompt  # 실제로는 OpenAI API를 호출하여 응답 생성 가능
            car_info = None  # 일반 차량 정보이므로 상세 정보는 없음
    else:
        # 차량 추천 내용이 아닌 경우 일반적인 OpenAI API 호출
        openai_history = [session_data["system_message"]] + conversation_history
        try:
            ai_response = get_openai_response(openai_history)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API 호출 중 오류 발생: {str(e)}")
        conversation_history.append({"role": "assistant", "content": ai_response})
        car_info = None

    # 사용되지 않은 세션 정리
    cleanup_sessions()

    # 최종 응답 반환
    return ChatResponse(
        response=ai_response,
        session_id=session_id,
        history=conversation_history,
        car_info=car_info
    )
