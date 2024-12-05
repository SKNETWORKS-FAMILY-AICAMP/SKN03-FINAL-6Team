import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document

# 1. FAISS Index 생성 함수
def create_faiss(embeddings):
    """
    주어진 임베딩 차원에 따라 새로운 FAISS Index를 생성합니다.
    """
    dimension_size = len(embeddings.embed_query("hello world"))

    db = FAISS(
        embedding_function=embeddings,
        index=faiss.IndexFlatL2(dimension_size),
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    return db

# 2. 문서를 벡터화하고 인덱스에 추가하는 함수
def add_documents(vectorDB, documents, ids):
    """
    주어진 문서를 FAISS 인덱스에 추가합니다.
    
    Parameters:
    - index: FAISS 인덱스 객체
    - documents: 추가할 문서 리스트
    - embedding_function: 임베딩 함수
    """
    # page_content, metadata 지정
    vectorDB.add_documents(
        documents,
        ids=ids,
    )
    return vectorDB

def save_faiss(vectorDB):
    # 로컬 Disk 에 저장
    vectorDB.save_local(folder_path="faiss_db", index_name="faiss_index")

def load_faiss(embeddings):
    loaded_db = FAISS.load_local(
        folder_path="E:\\SKN\\pdf\\faiss_db\\faiss_db",
        index_name="E:\\SKN\\pdf\\faiss_db\\faiss_index",
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )
    return loaded_db