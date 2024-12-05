import random
import time
import hashlib
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from recommend_car.apps.db import get_connection
from recommend_car.apps.utils import get_openai_response
from recommend_car.apps.prompt_manager import get_system_prompt

router = APIRouter()


# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,  
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # 터미널 출력
        logging.StreamHandler(),
        logging.FileHandler("chatbot.log"),  
    ],
)
logger = logging.getLogger("recommend_car")

# 메모리 저장소
conversation_memory = {}
# 세션 만료 시간 (1시간)
SESSION_EXPIRY_SECONDS = 3600

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
    car_ids: List[int] = Field(default=[])  # 차량 ID 목록 추가

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

# 사용되지 않은 세션 삭제(1시간 뒤에 삭제됨)
def cleanup_sessions():
    current_time = time.time()
    expired_sessions = [
        session_id
        for session_id, session_data in conversation_memory.items()
        if (current_time - session_data["last_access"]) > SESSION_EXPIRY_SECONDS
    ]
    for session_id in expired_sessions:
        logger.info(f"세션 {session_id} 만료로 삭제")
        del conversation_memory[session_id]

# 속성-테이블 및 컬럼 매핑 테이블 (추가 예정)
# 해당 keyword를 추출하여 검색하도록 설정
# 추가로 키워드 설정 예정
ATTRIBUTE_KEYWORDS = {
    '연비': ('car_detail_info', 'combined_fuel_efficiency'),
    '배터리 타입': ('car_detail_info', 'battery_type'),
    '배터리 제조사': ('car_detail_info', 'battery_manufacturer'),
    '연료 타입': ('car_detail_info', 'fuel'),
    '제조사': ('car', 'car_brand'),
    '브랜드': ('car', 'car_brand'),
    '이미지': ('car', 'car_image'), 
    '가격': ('car_detail_info', 'price'),
}

# 차량 이름 및 ID 목록 가져오기
def get_all_cars():
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "SELECT car_id, car_name FROM car"
            cursor.execute(sql)
            result = cursor.fetchall()
            logger.info(f"DB에서 가져온 차량 목록: {result}")
            return result
    except Exception as e:
        logger.error("❌ DB에서 차량 이름을 가져오는 중 오류 발생:", exc_info=True)
        return []
    finally:
        if connection:
            connection.close()
            logger.info("DB 연결 종료")

# 사용자 입력에서 모델명과 차량 ID, 속성 추출
def extract_model_and_attribute(user_input):
    # 차량 이름 및 ID 목록 가져오기
    cars = get_all_cars()
    model_name = None
    car_id = None
    for car in cars:
        if car["car_name"] in user_input:
            model_name = car["car_name"]
            car_id = car["car_id"]
            break

    # 속성 추출
    attribute_keyword = None
    for keyword in ATTRIBUTE_KEYWORDS.keys():
        if keyword in user_input:
            attribute_keyword = keyword
            break

    return model_name, car_id, attribute_keyword

# 차량 속성 정보 가져오기
def get_car_attribute(model_name, attribute_keyword):
    connection = None
    try:
        table_name, column_name = ATTRIBUTE_KEYWORDS[attribute_keyword]
        connection = get_connection()
        with connection.cursor() as cursor:
            if table_name == 'car':
                sql = f"SELECT {column_name} FROM car WHERE car_name = %s"
                cursor.execute(sql, (model_name,))
            elif table_name == 'car_detail_info':
                sql = f"""
                SELECT cdi.{column_name}
                FROM car_detail_info cdi
                JOIN car c ON c.car_id = cdi.car_id
                WHERE c.car_name = %s
                """
                cursor.execute(sql, (model_name,))
            else:
                return None
            result = cursor.fetchone()
            if result:
                return result[column_name]
            else:
                return None
    except Exception as e:
        logger.error("❌ DB에서 차량 속성 정보를 가져오는 중 오류 발생:", exc_info=True)
        return None
    finally:
        if connection:
            connection.close()
            logger.info("DB 연결 종료")

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

    # 사용자 질문에서 모델명, 차량 ID, 속성 추출
    model_name, car_id, attribute_keyword = extract_model_and_attribute(user_input)

    if model_name and attribute_keyword:
        # DB에서 해당 정보 가져오기
        attribute_value = get_car_attribute(model_name, attribute_keyword)
        if attribute_value:
            car_info_text = f"{model_name}의 {attribute_keyword}는 {attribute_value}입니다."
            logger.info(f"OpenAI에 전달할 차량 정보 컨텍스트: {car_info_text}")
        else:
            car_info_text = f"{model_name}의 {attribute_keyword} 정보를 찾을 수 없습니다."
            logger.warning(f"DB에서 {model_name}의 {attribute_keyword} 정보를 찾을 수 없습니다.")
    else:
        car_info_text = "질문에서 차량 모델명이나 요청하신 정보를 이해하지 못했습니다."
        logger.warning("모델명 또는 속성을 추출하지 못했습니다.")

    system_prompt = get_system_prompt()
    full_system_prompt = f"{system_prompt}\n\n{car_info_text}"
    openai_history = [{"role": "system", "content": full_system_prompt}] + conversation_history

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
        car_ids=[car_id] if car_id else []  # 차량 ID 추가
    )
