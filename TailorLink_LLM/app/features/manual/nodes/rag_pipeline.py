# from retriever import retrieve_documents
# from models.model import call_llm
from app.features.manual.utils.pdf_loader import pdf_load
from app.features.manual.utils.preprocess import clean_text
from app.features.manual.nodes.nodes import genesis_check, query_rewrite, vector_search, calculate_score,genesis_check_conditional,calculate_score_conditional

from langgraph.graph import StateGraph, START, END
from app.features.manual.utils.types import State

def run_rag(user_input: str, conversation_history: list = None) -> str:
    """
        RAG 파이프라인을 실행합니다.

        Args:
            user_input (str): 사용자 입력 질문.
            conversation_history (list): 이전 대화 기록 (선택적).

        Returns:
            str: RAG를 통해 생성된 최종 답변.
    """

    # 대화 히스토리와 현재 입력을 결합하여 컨텍스트 생성
    if conversation_history:
        context = "\n".join([f"{item['role']}: {item['content']}" for item in conversation_history])
        combined_input = f"{context}\nuser: {user_input}"
    else:
        combined_input = user_input

    graph_builder = StateGraph(State)

    graph_builder.add_node("genesis_check", genesis_check)
    graph_builder.add_node("vector_search", vector_search)
    graph_builder.add_node("calculate_score", calculate_score)
    graph_builder.add_node("query_rewrite", query_rewrite)

    graph_builder.add_edge(START, "genesis_check")
    graph_builder.add_edge('query_rewrite', "vector_search")
    graph_builder.add_edge('vector_search', "calculate_score")
    graph_builder.add_edge('query_rewrite', "vector_search")

    graph_builder.add_conditional_edges(
        'genesis_check',
        genesis_check_conditional,
        path_map={"search": "vector_search", END: END},
    )

    graph_builder.add_conditional_edges(
        "calculate_score",
        calculate_score_conditional,
        path_map={"rewrite": "query_rewrite", END: END},
    )

    graph = graph_builder.compile()

    state: State = {
        "message": user_input,
        "context": [],
        "answer": "",
        "change_count": 0,
        "is_valid_question": False,
        "is_pass": False,
        "previous_question": [],
        "best_answer": "",
        "best_score": 0,
    }
    res = graph.invoke(state)

    return res['best_answer']