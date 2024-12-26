# 그래프 파이프 라인 생성
from app.features.finance.models.model import get_OpenAI
from app.features.finance.nodes.nodes import (agent,
                                              Router,
                                              grade_documents,
                                              retriever_tool,
                                              rewrite, generate,
                                              conditional_decision,
                                              conditional_retriever,
                                              load_memorizer
)
from langgraph.graph import StateGraph, START, END
from app.features.finance.utils.types import State

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph


def run_finance_chatbot(user_input: str, car_id: int, history: list) -> str:
    """
        RAG 파이프라인을 실행합니다.

        Args:
            user_input (str): 사용자 입력 질문.
            conversation_history (list): 이전 대화 기록 (선택적).

        Returns:
            str: RAG를 통해 생성된 최종 답변.
    """
    workflow.add_node("agent", agent)
    # workflow.add_node("memorizer", memorizer)
    workflow.add_node("router", Router)
    workflow.add_node("retriever_tool", retriever_tool)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("rewrite", rewrite)
    workflow.add_node("generate", generate)


    workflow.add_edge(START, "router")
    # workflow.add_edge("load_memorizer", "router")

    workflow.add_edge("agent", END)
    workflow.add_edge("retriever_tool", "grade_documents")
    workflow.add_edge("generate", END)
    workflow.add_edge("rewrite", "router")
    
    workflow.add_conditional_edges(
        "router",
        conditional_retriever,
        path_map={
            "retriever_tool": "retriever_tool",
            "agent": "agent",
        },
    )
    
    workflow.add_conditional_edges(
        "grade_documents",
        # Assess agent decision
        conditional_decision,
        path_map={
            "generate": "generate",
            "rewrite": "rewrite",
        },
    )
    
    graph = workflow.compile(checkpointer=memory)

        
    state: State = {
        "message": user_input,
        "car_id": car_id,
        "retrieved_docs": {}, 
        "answer": [],
        "previous_question": [],
        "document_grading": [],
        "insurance_grading" : [],
        "rewritten_question" : [],
        "generated_response": [],
        "chat_history":history
    }
    res = graph.invoke(state)

    return res['answer']




