from typing import TypedDict, Optional, Literal

class AgentState(TypedDict):
    user_input: str  # 사용자의 원본 입력
    final_result: Optional[list[dict]]  # 최종 추천 결과
    response: Optional[str]  # 모델이 생성한 응답
    suggested_questions: Optional[list[str]]  # 예상 질문 리스트
    page_info: Optional[dict[str, str]]

