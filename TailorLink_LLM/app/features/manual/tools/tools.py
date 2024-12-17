from langchain.tools import tool
from app.features.manual.tools.milvus_search import dense_search, hybrid_search, sparse_search
from app.features.manual.models.embedding import generate_query_embeddings
from app.database.milvus import get_collection

MILVUS_COLLECTION_NAME = "manual"  # 설정값으로 분리

@tool
def search_milvus(query: str, sparse_weight: float = 0.7, dense_weight: float = 1.0, limit: int = 10) -> list:
    """
    Perform a hybrid search in the Milvus vector database.

    This function combines sparse and dense embeddings to retrieve the most relevant results.

    Args:
        query (str): The input query string.
        sparse_weight (float, optional): Weight for sparse embeddings. Default is 0.7.
        dense_weight (float, optional): Weight for dense embeddings. Default is 1.0.
        limit (int, optional): The maximum number of search results to retrieve. Default is 10.

    Returns:
        list: A list of retrieved search results from Milvus.

    Raises:
        ValueError: If the input query is empty or invalid.
    """

    # Generate query embeddings
    query_embeddings = generate_query_embeddings([query])
    if not query_embeddings:
        raise RuntimeError("Failed to generate query embeddings.")

    # Retrieve the Milvus collection
    collection = get_collection(MILVUS_COLLECTION_NAME)

    results = hybrid_search(
        col=collection,
        query_dense_embedding=query_embeddings["dense"][0],
        query_sparse_embedding=query_embeddings["sparse"]._getrow(0),
        sparse_weight=sparse_weight,
        dense_weight=dense_weight,
    )
    return results
