import time
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from langchain_community.agent_toolkits import create_sql_agent
from pydantic import BaseModel
from datetime import datetime
import json
import asyncio
from fastapi.responses import StreamingResponse

from app.core.logger import logger
from app.utils.session_manager import generate_session_id, initialize_session, update_session_access,cleanup_sessions

from app.database.chat_history import ChatHistoryManager, Session
from langchain_core.messages import HumanMessage, AIMessage

# 세션 및 매니저 초기화
session = Session()
chat_history_manager = ChatHistoryManager(session)

from app.features.manual.nodes.rag_pipeline import run_manual_chatbot, test_rag
manual_qa_router = APIRouter()

conversation_memory = {}
SESSION_EXPIRY_SECONDS = 3600

class Message(BaseModel):
    role: str = Field(...)
    content: str = Field(...)

class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(None)
    user_id: Optional[str] = Field(None)
    user_input: str = Field(...)
    car_id: int = Field(...)

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI의 최종 응답 텍스트")
    session_id: str = Field(..., description="현재 세션 ID")
    agent_id: str = Field(..., description="기능 설명")
    response_type: str = Field(..., description="응답 유형 (e.g., 사용자, ai)")
    page_info: dict = Field(None, description="도구에서 반환된 key-value 결과")
    suggest_question: list = Field(..., description="예상 질문")
    timestamp: datetime = Field(..., description="응답 생성 시각")

@manual_qa_router.post("/manual", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    logger.info('Running manaul chatbot')

    # 세션ID가 없으면 생성
    session_id = chat_request.session_id or generate_session_id()
    user_id = chat_request.user_id
    user_input = chat_request.user_input
    car_id = chat_request.car_id

    logger.info(f'user_id: {user_id}\n session_id: {session_id} \n')

    chat_history_manager.save_message(
        session_id=session_id,
        user_id=user_id,
        message=HumanMessage(content=user_input),
        message_type="human"
    )

    conversation_history =  chat_history_manager.load_history(session_id)

    agent_id = "manual"
    # 기본값 초기화
    response_type = ""
    page_info = {
        "car_id" : "",
        "car_name": "",
        "car_image": "",    
    }
    timestamp = datetime.now()

    res = run_manual_chatbot(user_input, car_id, conversation_history)

    # AI 응답 추가
    chat_history_manager.save_message(
        session_id=session_id,
        user_id=user_id,
        message=AIMessage(content=res),
        message_type="ai"
    )

    return ChatResponse(
        response=res,
        session_id=session_id,
        response_type=response_type,
        agent_id=agent_id,
        page_info=page_info,
        suggest_question=[],
        timestamp=timestamp
    )

# @manual_qa_router.post("/manual", response_model=ChatResponse)
# async def ask_query(chat_request: ChatRequest):
#     question = chat_request.user_input
#     print(question)
#     async def mock_stream_openai_response(prompt):
#         accumulated_text = ""  # 누적 텍스트 저장
#         res = run_rag(prompt)
#         print(type(res))
#         for letter in res:
#             accumulated_text += letter  # 텍스트 누적
#             yield json.dumps({"status": "processing", "data": letter}, ensure_ascii=False) + "\n"
#             await asyncio.sleep(0.05)  # 스트림 딜레이 시뮬레이션
#
#         yield json.dumps({"status": "complete", "data": "Stream finished"}, ensure_ascii=False) + "\n"
#
#     return StreamingResponse(mock_stream_openai_response(question), media_type="text/event-stream")


