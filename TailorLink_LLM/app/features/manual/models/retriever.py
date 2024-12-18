from langchain_milvus.retrievers import MilvusCollectionHybridSearchRetriever
from app.database.milvus import get_collection
from pymilvus import WeightedRanker
from app.features.manual.models.embedding import sparse_embedding_func, dense_embedding_func
MILVUS_COLLECTION_NAME = "manual"  # 설정값으로 분리

sparse_search_params = {"metric_type": "IP"}
dense_search_params = {"metric_type": "IP", "params": {}}

collection = get_collection(MILVUS_COLLECTION_NAME)

def get_milvus_hybrid_search_retriever(sparse_weight: float = 0.5, dense_weight: float = 0.5, limit: int = 3):

    dense_field = "dense_vector"
    sparse_field = "sparse_vector"
    text_field = "text"
    retriever = MilvusCollectionHybridSearchRetriever(
        collection=collection,
        rerank=WeightedRanker(sparse_weight, dense_weight),
        anns_fields=[dense_field, sparse_field],
        field_embeddings=[dense_embedding_func, sparse_embedding_func],
        field_search_params=[dense_search_params, sparse_search_params],
        top_k=limit,
        text_field=text_field,
    )
    return retriever