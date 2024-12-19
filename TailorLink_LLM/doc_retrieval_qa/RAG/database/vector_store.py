from RAG.database.milvus_connector import get_collection
from RAG.llm.embedding import generate_embedding

def save_to_milvus(collection_name, document_id, processed_text):
    # Milvus에 저장
    collection = get_collection(collection_name)
    embedding = generate_embedding([processed_text])

    data = []
    # embedding['dense']가 list 형태인지 확인하고 저장
    if isinstance(embedding['dense'], list):
        # embedding['dense']가 중첩 리스트인 경우 일차원 리스트로 변환
        flattened_vector = [item for sublist in embedding['dense'] for item in
                            (sublist if isinstance(sublist, list) else [sublist])]
        data.append({"document_id": document_id, "vector": flattened_vector})
    else:
        raise TypeError("Embedding should be a list of floats.")

    # collection.insert 호출 시 collection_name 대신 entities만 전달
    collection.insert(data=data)
    print(f"Saved embedding for {document_id} to Milvus.")