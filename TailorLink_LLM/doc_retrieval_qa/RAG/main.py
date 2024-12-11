# from rag_pipeline import run_rag
from database.milvus_connector import connect_to_milvus
from rag_pipeline import process_pdf_and_store, run_rag
if __name__ == "__main__":
    # Milvus 연결 초기화
    connect_to_milvus()

    # process_pdf_and_store('../data/documents/genesis-g90-black-24-manual-kor.pdf', 'genesis')

    a = run_rag('시동 거는 법')
    print(a)