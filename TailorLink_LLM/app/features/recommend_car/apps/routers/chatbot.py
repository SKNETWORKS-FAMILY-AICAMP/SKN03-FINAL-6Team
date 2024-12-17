import random
import time
import hashlib
import logging
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from langchain_community.agent_toolkits import create_sql_agent
from pydantic import BaseModel
from datetime import datetime
from ..utils import connect_aws_db
from ..prompt_manager import get_prompt
from ..cilent import get_client
#나중에 수정해야함.
# from ..workflow import build_workflow

car_recommend_router = APIRouter()

conversation_memory = {}
SESSION_EXPIRY_SECONDS = 3600

class Message(BaseModel):
    role: str = Field(...)
    content: str = Field(...)

class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(None)
    user_input: str = Field(...)

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI의 최종 응답 텍스트")
    session_id: str = Field(..., description="현재 세션 ID")
    agent_id: str = Field(..., description="기능 설명")
    response_type: str = Field(..., description="응답 유형 (e.g., 사용자, ai)")
    page_info: dict[str, str] = Field(..., description="도구에서 반환된 key-value 결과")
    suggest_question: list = Field(..., description="예상 질문")
    timestamp: datetime = Field(..., description="응답 생성 시각")

def generate_session_id() -> str:
    while True:
        random_number = random.randint(1000000000, 9999999999)
        session_id = hashlib.sha256(str(random_number).encode()).hexdigest()[:16]
        if session_id not in conversation_memory:
            return session_id

def initialize_session(session_id):
    if session_id not in conversation_memory:
        conversation_memory[session_id] = {
            "last_access": time.time(),
            "history": [],
        }

def cleanup_sessions():
    current_time = time.time()
    expired_sessions = [
        session_id
        for session_id, session_data in conversation_memory.items()
        if (current_time - session_data["last_access"]) > SESSION_EXPIRY_SECONDS
    ]
    for session_id in expired_sessions:
        del conversation_memory[session_id]

@car_recommend_router.post("/car_recommend_chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    session_id = chat_request.session_id or generate_session_id()
    user_input = chat_request.user_input

    initialize_session(session_id)
    session_data = conversation_memory[session_id]
    session_data["last_access"] = time.time()
    conversation_history = session_data["history"]

    conversation_history.append({"role": "user", "content": user_input})
    agent_id = "recommend_car"
    # 기본값 초기화
    response_type = ""
    page_info = {
        "car_id" : "",
        "car_name": "",
        "car_image": "",    
    }
    timestamp = datetime.now()
    suggest_question = []
    try:
        # Tool 사용
        agent_runnable = create_sql_agent(
            get_client(),
            db=connect_aws_db(),
            agent_type="openai-tools",
            verbose=True,
            prompt=get_prompt()
        )
        agent_outcome = agent_runnable.invoke(user_input)
        # Tool 관련 데이터 추출
        page_info = agent_outcome.get("page_info", {
            "car_id": "",
            "car_name": "",
            "car_image": ""
        })  # page_info가 없을 때 기본값 설정
        suggest_question = agent_outcome.get("suggest_question", [])  # 예상 질문 추출
        ai_response = agent_outcome.get("output", "요청을 처리할 수 없습니다.")  # 기본 응답 설정
        response_type = "ai"
        
    except Exception as e:
        logging.error(e)
        ai_response = "죄송합니다. 요청을 처리하는 중 문제가 발생했습니다."
        response_type = "error"


    if not page_info:
        page_info = {
                "car_id" : "",
                "car_name": "",
                 "car_image": "",
                }
    # 대화 이력에 응답 추가
    conversation_history.append({"role": "assistant", "content": ai_response})
    cleanup_sessions()

    return ChatResponse(
        response=ai_response,
        session_id=session_id,
        agent_id=agent_id,
        response_type=response_type,
        page_info=page_info,
        suggest_question=suggest_question,
        timestamp=timestamp
    )
