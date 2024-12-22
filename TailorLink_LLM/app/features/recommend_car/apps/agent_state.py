from typing import TypedDict, Optional, Literal

class AgentState(TypedDict):
    user_input: str  # 사용자의 원본 입력
    generated_query: Optional[str]  # 생성된 SQL 쿼리
    db_result: Optional[list[dict]]  # DB 검색 결과
    milvus_result: Optional[list[dict]]  # Milvus 검색 결과
    final_result: Optional[list[dict]]  # 최종 추천 결과
    response: Optional[str]  # 모델이 생성한 응답
    suggested_questions: Optional[list[str]]  # 예상 질문 리스트
    page_info: Optional[dict[str, str]]  # 사용자에게 반환할 페이지 정보
    input_filtered: Optional[bool]  # 입력 필터링 여부
    search_exhausted: Optional[bool]  # 검색 결과 없음 여부

