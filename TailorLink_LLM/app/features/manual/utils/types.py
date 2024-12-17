from typing import TypedDict, Optional, List
from typing import Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    message: str
    context: list
    answer: str
    change_count: int
    is_valid_question: bool
    is_pass:bool
    previous_question: list
    best_answer: str
    best_score: int

