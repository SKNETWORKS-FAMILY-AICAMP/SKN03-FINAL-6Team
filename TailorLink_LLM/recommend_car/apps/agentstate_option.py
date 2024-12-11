from typing import TypedDict, Annotated, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    input: str
    # 대화 내용 중 '이전 메시지' 목록
    chat_history: list[BaseMessage] 
    # 유효한 유형으로 `None`이 필요
    agent_outcome: Union[AgentAction, AgentFinish, None] 
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]