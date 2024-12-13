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

logging.basicConfig(
    level=logging.DEBUG,  
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("chatbot.log"),  
    ],
)
logger = logging.getLogger("recommend_car")

conversation_memory = {}
SESSION_EXPIRY_SECONDS = 3600

class Message(BaseModel):
    role: str = Field(...)
    content: str = Field(...)

class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(None)
    user_input: str = Field(...)

class ToolResult(BaseModel):
    key: str
    value: str

class LangGraph(BaseModel):
    tool_used: bool
    source: str  # e.g., 'tool/db/self'

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI의 최종 응답 텍스트")
    session_id: str = Field(..., description="현재 세션 ID")
    history: list[Message] = Field(..., description="대화 이력")
    car_details: Optional[list[dict]] = Field(default=[], description="추천된 차량의 상세 정보")
    response_type: str = Field(..., description="응답 유형 (e.g., informative, warning)")
    tool_result: Optional[dict] = Field(None, description="도구에서 반환된 key-value 결과")
    text: str = Field(..., description="도구 사용 여부에 따라 생성된 텍스트")
    langgraph: LangGraph = Field(..., description="언어 그래프 정보 (도구 사용 여부 및 소스)")
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
        logger.info(f"세션 {session_id} 초기화 완료")

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

@car_recommend_router.post("/car_recommend_chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    session_id = chat_request.session_id or generate_session_id()
    user_input = chat_request.user_input

    logger.info(f"새로운 요청 - 세션 ID: {session_id}, 사용자 입력: {user_input}")

    initialize_session(session_id)
    session_data = conversation_memory[session_id]
    session_data["last_access"] = time.time()
    conversation_history = session_data["history"]

    conversation_history.append({"role": "user", "content": user_input})
    logger.info(f"대화 이력 업데이트 - 현재 이력: {conversation_history}")

    # 기본값 초기화
    response_type = "informative"
    tool_result = None
    text = ""
    langgraph = {"tool_used": False, "source": "self"}
    timestamp = datetime.now()
    car_details = []
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
        ai_response = agent_outcome["output"]

        # Tool 관련 데이터 추출
        tool_result = agent_outcome.get("tool_result", {})  # e.g., key-value 결과
        text = ai_response
        langgraph = {"tool_used": True, "source": "tool/db"}

    except Exception as e:
        logger.error("오류 발생", exc_info=True)
        ai_response = "죄송합니다. 요청을 처리하는 중 문제가 발생했습니다."
        response_type = "error"
        text = ai_response

    # 대화 이력에 응답 추가
    conversation_history.append({"role": "assistant", "content": ai_response})
    cleanup_sessions()
    logger.info(f"세션 {session_id} 정리 완료")

    return ChatResponse(
        response=ai_response,
        session_id=session_id,
        history=conversation_history,
        car_details=car_details,
        response_type=response_type,
        tool_result=tool_result,
        text=text,
        langgraph=LangGraph(**langgraph),
        timestamp=timestamp
    )
