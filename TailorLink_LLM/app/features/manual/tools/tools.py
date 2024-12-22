from langchain.tools import tool
from app.features.manual.tools.milvus_search import dense_search, hybrid_search, sparse_search
from app.features.manual.models.embedding import generate_query_embeddings
from app.database.milvus import get_collection
from app.features.manual.models.reranker import bge_rf

MILVUS_COLLECTION_NAME = "manual"  # 설정값으로 분리

@tool
def search_milvus(query_list: list, sparse_weight: float = 0.5, dense_weight: float = 0.5, limit: int = 10) -> list:
    """
    Perform a hybrid search in the Milvus vector database.

    This function combines sparse and dense embeddings to retrieve the most relevant results.

    Args:
        query (list): The input query string.
        sparse_weight (float, optional): Weight for sparse embeddings. Default is 0.7.
        dense_weight (float, optional): Weight for dense embeddings. Default is 1.0.
        limit (int, optional): The maximum number of search results to retrieve. Default is 10.

    Returns:
        list: A list of retrieved search results from Milvus.

    Raises:
        ValueError: If the input query is empty or invalid.
    """

    # Generate query embeddings
    query_embeddings = generate_query_embeddings(query_list)
    if not query_embeddings:
        raise RuntimeError("Failed to generate query embeddings.")

    # Retrieve the Milvus collection
    collection = get_collection(MILVUS_COLLECTION_NAME)

    results_list = []
    for index, query in enumerate(query_list):
        results = hybrid_search(
            col=collection,
            query_dense_embedding=query_embeddings["dense"][index],
            query_sparse_embedding=query_embeddings["sparse"]._getrow(index),
            sparse_weight=sparse_weight,
            dense_weight=dense_weight,
            limit=limit,
        )

        rerank_results = bge_rf(
            query=query,
            documents=results,
            top_k=3,
        )
        results_list.append(rerank_results)

    return results_list
