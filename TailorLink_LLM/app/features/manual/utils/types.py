from typing import TypedDict, Optional, List
from typing import Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    car_id:int
    message: str               # 사용자 질문
    questions: list            # 사용자 질문 분리 리스트
    context: list              # 참고 문서
    answer: str                # 생성 답변
    change_count: int          # 변경 횟수
    is_stop:bool
    previous_question: list
    best_answer: str
    best_score: int
    chat_history: list

