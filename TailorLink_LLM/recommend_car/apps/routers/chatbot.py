import random
import time
import hashlib
import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from recommend_car.apps.db import get_connection  
from recommend_car.apps.utils import get_openai_response
from recommend_car.apps.prompt_manager import get_system_prompt

router = APIRouter()

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,  # DEBUG, INFO, WARNING 등 필요에 따라 설정
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # 터미널 출력
        logging.FileHandler("chatbot.log"),  # 로그 파일 저장
    ],
)
logger = logging.getLogger("recommend_car")  # 고유한 로거 이름 지정

# 메모리 저장소
conversation_memory = {}
SESSION_EXPIRY_SECONDS = 3600  # 세션 만료 시간 (1시간)

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

# SHA256 해싱으로 고유한 세션 ID 생성
def generate_session_id() -> str:
    while True:
        random_number = random.randint(1000000000, 9999999999)
        session_id = hashlib.sha256(str(random_number).encode()).hexdigest()[:16]
        if session_id not in conversation_memory:
            return session_id

# 세션 초기화
def initialize_session(session_id):
    if session_id not in conversation_memory:
        conversation_memory[session_id] = {
            "last_access": time.time(),
            "history": [],
        }
        logger.info(f"세션 {session_id} 초기화 완료")

# 사용되지 않은 세션 삭제
def cleanup_sessions():
    current_time = time.time()
    expired_sessions = [
        session_id
        for session_id, session_data in conversation_memory.items()
        if (current_time - session_data["last_access"]) > SESSION_EXPIRY_SECONDS
    ]
    for session_id in expired_sessions:
        logger.info(f"세션 {session_id} 만료로 삭s제")
        del conversation_memory[session_id]

# 차량 정보 검색
def get_all_cars():
    connection = None
    try:
        # DB 연결 시도
        connection = get_connection()
        if connection is None:
            logger.error("❌ DB 연결 객체가 None입니다.")
            return []

        with connection.cursor() as cursor:
            sql = "SELECT car_name FROM car"
            cursor.execute(sql)
            result = [row["car_name"] for row in cursor.fetchall()]
            logger.info(f"DB에서 가져온 차량 목록: {result}")
            return result
    except Exception as e:
        logger.error("❌ DB 검색 오류:", exc_info=True)
        return []
    finally:
        if connection:  # connection이 None이 아닐 때만 닫음
            try:
                connection.close()
                logger.info("DB 연결 종료")
            except Exception as close_error:
                logger.error("DB 연결 종료 중 오류 발생", exc_info=True)

@router.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    # 세션 ID 생성 또는 가져오기
    session_id = chat_request.session_id or generate_session_id()
    user_input = chat_request.user_input

    logger.info(f"새로운 요청 - 세션 ID: {session_id}, 사용자 입력: {user_input}")

    # 세션 초기화
    initialize_session(session_id)

    # 세션 데이터 가져오기
    session_data = conversation_memory[session_id]
    session_data["last_access"] = time.time()
    conversation_history = session_data["history"]

    # 사용자 입력 추가
    conversation_history.append({"role": "user", "content": user_input})
    logger.info(f"대화 이력 업데이트 - 현재 이력: {conversation_history}")

    # DB에서 차량 이름 목록 가져오기
    car_names = get_all_cars()
    if car_names:
        logger.info(f"DB에서 차량 정보 조회 성공: {car_names}")
    else:
        logger.warning("DB에서 차량 정보를 찾을 수 없습니다.")

    # OpenAI에게 전달할 메시지 구성
    system_prompt = get_system_prompt()
    openai_history = [{"role": "system", "content": system_prompt}] + conversation_history

    try:
        ai_response = get_openai_response(openai_history)
        logger.info(f"OpenAI 응답: {ai_response}")
    except Exception as e:
        logger.error("OpenAI 호출 중 오류 발생", exc_info=True)
        raise HTTPException(status_code=500, detail=f"OpenAI API 호출 중 오류 발생: {str(e)}")

    # 응답 추가
    conversation_history.append({"role": "assistant", "content": ai_response})
    cleanup_sessions()
    logger.info(f"세션 {session_id} 정리 완료")

    return ChatResponse(
        response=ai_response,
        session_id=session_id,
        history=conversation_history,
    )
