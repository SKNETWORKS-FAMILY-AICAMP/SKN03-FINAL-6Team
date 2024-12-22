import hashlib
import random
import logging
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.features.recommend_car.apps.workflow import build_car_recommendation_workflow
from app.features.recommend_car.apps.agent_state import AgentState  # AgentState 추가

car_recommend_router = APIRouter()

class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(None)
    user_input: str = Field(...)

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI의 최종 응답 텍스트")
    session_id: str = Field(..., description="현재 세션 ID")
    agent: str = Field(..., description="기능 설명")
    response_type: str = Field(..., description="응답 유형 (e.g., 사용자, ai)")
    page_info: dict[str, str] = Field(..., description="도구에서 반환된 key-value 결과")
    suggest_question: list = Field(..., description="예상 질문")
    timestamp: datetime = Field(..., description="응답 생성 시각")

def generate_session_id() -> str:
    """세션 ID 생성"""
    random_number = random.randint(1000000000, 9999999999)
    return hashlib.sha256(str(random_number).encode()).hexdigest()[:16]

@car_recommend_router.post("/car_recommend_chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    """
    차량 추천 워크플로우 실행 및 응답 반환
    """
    session_id = chat_request.session_id or generate_session_id()
    user_input = chat_request.user_input

    agent_id = "recommend_car"
    timestamp = datetime.now()

    # 기본값 초기화
    response = "죄송합니다. 요청을 처리하는 중 문제가 발생했습니다."
    page_info = {"car_id": "", "car_name": "", "car_image": ""}
    suggest_question = []
    response_type = "error"

    try:
        # 워크플로우 실행
        workflow = build_car_recommendation_workflow()

        # 초기 상태 생성
        initial_state: AgentState = {
            "user_input": user_input,
            "generated_query": None,
            "db_result": [],
            "milvus_result": [],
            "final_result": [],
            "response": "",
            "suggested_questions": [],
            "page_info": {},
            "input_filtered": False,  
            "search_exhausted": False 
        }

        # 워크플로우 실행 및 상태 갱신
        workflow_result: AgentState = workflow.invoke(
            initial_state,
            config={"configurable": {"thread_id": session_id}}
        )

        # 결과 처리
        response = workflow_result["response"]
        final_results = workflow_result.get("final_result", [])

        # page_info 할당
        if final_results:
            top_result = final_results[0]
            page_info = {
                "car_id": str(top_result.get("car_id", "")),
                "car_name": top_result.get("car_name", ""),
                "car_image": top_result.get("car_image", "")
            }

        # 예상 질문 할당
        suggest_question = workflow_result.get("suggested_questions", [])
        response_type = "ai"

    except Exception as e:
        logging.error(f"[ERROR] Chat 요청 처리 중 오류 발생: {e}", exc_info=True)

    return ChatResponse(
        response=response,
        session_id=session_id,
        agent=agent_id,
        response_type=response_type,
        page_info=page_info,
        suggest_question=suggest_question,
        timestamp=timestamp
    )
