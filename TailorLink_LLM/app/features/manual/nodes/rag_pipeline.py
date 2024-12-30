from app.features.manual.models.model import create_openai_model
from app.features.manual.nodes.nodes import (
        generate_history_base_answer,
        genesis_check_and_query_split,
        generate_vector_search_base_answer,
        grade_hallucination,
        grade_hallucination_conditional,
        calculate_score,
        query_rewrite,
        history_base_answer_check_conditional,
        genesis_check_conditional,
        calculate_score_conditional
)
from langgraph.graph import StateGraph, START, END
from app.features.manual.utils.types import State

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph


def run_manual_chatbot(user_input: str, car_id: int, history: list) -> str:
    """
        RAG 파이프라인을 실행합니다.

        Args:
            user_input (str): 사용자 입력 질문.
            conversation_history (list): 이전 대화 기록 (선택적).

        Returns:
            str: RAG를 통해 생성된 최종 답변.
    """
    graph_builder = StateGraph(State)
    graph_builder.add_node("generate_history_base_answer", generate_history_base_answer)
    graph_builder.add_node("genesis_check", genesis_check_and_query_split)
    graph_builder.add_node("generate_vector_search_base_answer", generate_vector_search_base_answer)
    graph_builder.add_node("grade_hallucination", grade_hallucination)
    graph_builder.add_node("calculate_score", calculate_score)
    graph_builder.add_node("query_rewrite", query_rewrite)

    graph_builder.add_edge(START, "genesis_check")

    graph_builder.add_edge('query_rewrite', "generate_vector_search_base_answer")
    graph_builder.add_edge('generate_vector_search_base_answer', "grade_hallucination")
    graph_builder.add_edge('query_rewrite', "generate_vector_search_base_answer")

    graph_builder.add_conditional_edges(
        'generate_history_base_answer',
        history_base_answer_check_conditional,
        path_map={"search": "generate_vector_search_base_answer", END: END},
    )

    graph_builder.add_conditional_edges(
        'genesis_check',
        genesis_check_conditional,
        path_map={"write": "generate_history_base_answer", END: END},
    )

    graph_builder.add_conditional_edges(
        'grade_hallucination',
        grade_hallucination_conditional,
        path_map={"rewrite": "query_rewrite", 'calculate': "calculate_score"},
    )

    graph_builder.add_conditional_edges(
        "calculate_score",
        calculate_score_conditional,
        path_map={"rewrite": "query_rewrite", END: END},
    )
    graph = graph_builder.compile()

    state: State = {
        "message": user_input,
        "car_id": car_id,
        "questions":[],
        "context": [],
        "answer": "",
        "change_count": 0,
        "is_valid_question": False,
        "is_pass": False,
        "previous_question": [],
        "best_answer": "",
        "best_score": 0,
        "chat_history":history
    }
    res = graph.invoke(state)

    return res['answer']

def test_rag(user_input, session):
    # Define a new graph
    workflow = StateGraph(state_schema=MessagesState)

    # Define the function that calls the model
    def call_model(state: MessagesState):
        llm = create_openai_model()
        response = llm.invoke(state["messages"])
        # Update message history with response:
        return {"messages": response}

    # Define the (single) node in the graph
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    # Add memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    config = {"configurable": {"thread_id": session}}
    res = app.invoke(user_input, config)
    return res["messages"][-1].pretty_print()