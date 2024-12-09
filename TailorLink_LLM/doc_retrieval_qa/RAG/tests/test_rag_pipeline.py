
from RAG.utils.pdf_loader import load_pdf
from RAG.utils.preprocess import clean_text, chunk_text
from RAG.database.milvus_connector import connect_to_milvus
from RAG.database.vector_store import save_to_milvus


def process_pdf_and_store(file_path, collection_name):
    """
    PDF 파일에서 텍스트를 추출, 전처리하고 Milvus에 임베딩 저장.
    """
    # Milvus 연결 초기화
    connect_to_milvus()

    # 1. PDF에서 텍스트 추출
    raw_text = load_pdf(file_path)
    if not raw_text:
        raise ValueError("Failed to extract text from PDF.")

    # 2. 텍스트 전처리
    processed_text = clean_text(raw_text)

    # 3. 텍스트 청킹
    chunks = chunk_text(processed_text, chunk_size=100, overlap=20)


    # 4. 임베딩 생성 및 Milvus 저장
    document_id = file_path.split('/')[-1]
    save_to_milvus(collection_name, document_id, processed_text)

    print(f"Document {document_id} stored in Milvus")