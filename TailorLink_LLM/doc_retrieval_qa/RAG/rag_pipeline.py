# from retriever import retrieve_documents
# from llm.model import call_llm
from RAG.utils.pdf_loader import pdf_load
from RAG.utils.preprocess import clean_text
from RAG.database.milvus_connector import connect_to_milvus
from RAG.database.vector_store import save_to_milvus
from RAG.nodes.nodes import genesis_check, query_rewrite, vector_search, calculate_score,genesis_check_conditional,calculate_score_conditional

from langgraph.graph import StateGraph, START, END
from RAG.types import State

def run_rag(query):
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
        "message": query,
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

def process_pdf_and_store(file_path, collection_name):
    """
    PDF 파일에서 텍스트를 추출, 전처리하고 Milvus에 임베딩 저장.
    """
    # Milvus 연결 초기화
    connect_to_milvus()

    # 1. PDF에서 텍스트 추출
    raw_text = pdf_load(file_path)
    if not raw_text:
        raise ValueError("Failed to extract text from PDF.")

    # 2. 텍스트 전처리
    processed_text = clean_text(raw_text)

    # 3. 임베딩 생성 및 Milvus 저장
    document_id = file_path.split('/')[-1]
    save_to_milvus(collection_name, document_id, processed_text)

    print(f"Document {document_id} stored in Milvus")