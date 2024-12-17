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
import json
import asyncio
from fastapi.responses import StreamingResponse

from doc_retrieval_qa.RAG.rag_pipeline import run_rag
from core.milvus_connector import connect_to_milvus
manual_qa_router = APIRouter()

conversation_memory = {}
SESSION_EXPIRY_SECONDS = 3600

class Message(BaseModel):
    role: str = Field(...)
    content: str = Field(...)

class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(None)
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

@manual_qa_router.post("/manual_qa", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    connect_to_milvus()
    session_id = chat_request.session_id or generate_session_id()
    user_input = chat_request.user_input

    initialize_session(session_id)
    session_data = conversation_memory[session_id]
    session_data["last_access"] = time.time()
    conversation_history = session_data["history"]

    conversation_history.append({"role": "user", "content": user_input})

    agent_id = "manual_qa"
    # 기본값 초기화
    response_type = ""
    page_info = {
        "car_id" : "",
        "car_name": "",
        "car_image": "",    
    }
    timestamp = datetime.now()

    res = run_rag(user_input)

    cleanup_sessions()

    return ChatResponse(
        response=res,
        session_id=session_id,
        response_type=response_type,
        agent_id=agent_id,
        page_info=page_info,
        suggest_question=[],
        timestamp=timestamp
    )
@manual_qa_router.post("/manual", response_model=ChatResponse)
async def ask_query(chat_request: ChatRequest):
    question = chat_request.user_input
    print(question)
    async def mock_stream_openai_response(prompt):
        accumulated_text = ""  # 누적 텍스트 저장
        res = run_rag(prompt)
        print(type(res))
        for letter in res:
            accumulated_text += letter  # 텍스트 누적
            yield json.dumps({"status": "processing", "data": letter}, ensure_ascii=False) + "\n"
            await asyncio.sleep(0.05)  # 스트림 딜레이 시뮬레이션

        yield json.dumps({"status": "complete", "data": "Stream finished"}, ensure_ascii=False) + "\n"

    return StreamingResponse(mock_stream_openai_response(question), media_type="text/event-stream")