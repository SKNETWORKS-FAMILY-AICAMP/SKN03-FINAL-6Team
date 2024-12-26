from typing_extensions import Annotated, Sequence, TypedDict
from langgraph.graph.message import add_messages
from langchain.schema import BaseMessage

class state(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    # 메시지 관리 (사용자와 시스템의 대화 기록)
    messages: Annotated[Sequence[BaseMessage], "add_messages"]
    # 세션 ID (각 워크플로우 인스턴스에 고유한 ID)
    session_id: str
    # 기타 메타데이터 (사용자 정보, 소스 등)
    metadata: dict
    # 검색된 문서 리스트
    retrieved_docs: dict  # 검색 결과 (MultiQueryRetriever의 반환 값)
    # 답변
    answer: list
    # 이전 질문
    previous_question: list
    # 문서 등급
    document_grading: list
    # 보험 등급
    insurance_grading : list
    # 재 생성 된 답변
    rewritten_question : list
    # 생성된 최종 답변
    generated_response: list  # 시스템의 최종 답변

