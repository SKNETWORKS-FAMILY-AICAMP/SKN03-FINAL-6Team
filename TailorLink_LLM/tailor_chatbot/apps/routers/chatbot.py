from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter()

from pydantic import BaseModel, Field
from typing import Optional, List

conversation_memory = {}

class Message(BaseModel):
    role: str = Field(..., description="The role of the message sender")
    content: str = Field(..., description="The content of the message")

class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(None, description="Session ID for the chat")
    user_input: str = Field(..., description="The user's input message")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The chatbot's response")
    session_id: str = Field(..., description="The session ID for the chat")
    history: List[Message] = Field(..., description="The chat history")


@router.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    # 세션 ID 확인
    session_id = chat_request.session_id or "default-session-id"
    user_input = chat_request.user_input

    # 세션 초기화
    if session_id not in conversation_memory:
        conversation_memory[session_id] = []

    conversation_history = conversation_memory[session_id]

    # 시스템 메시지 추가 (최초 요청 시)
    if not conversation_history:
        conversation_history.append(Message(role="system", content="안녕하세요, 저는 자동차 추천 챗봇입니다."))

    # 사용자 메시지 추가
    conversation_history.append(Message(role="user", content=user_input))

    # OpenAI 호출 생략
    ai_response = "자동차 추천 예시입니다. 어떤 모델을 선호하시나요?"
    conversation_history.append(Message(role="assistant", content=ai_response))

    # 응답 생성
    return ChatResponse(
        response=ai_response,
        session_id=session_id,
        history=conversation_history
    )
