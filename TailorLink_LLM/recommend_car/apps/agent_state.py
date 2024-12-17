from typing import TypedDict, Optional


class AgentState(TypedDict):
    user_input: str
    processed_input: Optional[str]
    generated_query: Optional[str]
    db_result: Optional[list[dict]]
    milvus_result: Optional[list[dict]]
    final_result: Optional[list[dict]]
    response: Optional[str]
    suggested_questions: Optional[list[str]]  # 이름 수정

