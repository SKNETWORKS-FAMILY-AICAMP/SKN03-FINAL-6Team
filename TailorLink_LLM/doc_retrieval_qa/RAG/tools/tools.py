from langchain.tools import tool
from doc_retrieval_qa.RAG.tools.milvus_search import dense_search, hybrid_search, sparse_search
from doc_retrieval_qa.RAG.llm.embedding import generate_query_embedding
from core.milvus_connector import get_collection


@tool
def search_milvus(query: str) -> list:
    """
    Search in the Milvus vector database using hybrid search.
    Combines dense and sparse embeddings for improved results.

    Args:
        query (str): The input query string.

    Returns:
        list: A list of search results from Milvus.
    """
    query_embeddings = generate_query_embedding([query])
    hybrid_results = hybrid_search(
        get_collection('manual'),
        query_embeddings["dense"][0],
        query_embeddings["sparse"]._getrow(0),
        sparse_weight=0.7,
        dense_weight=1.0,
    )
    return hybrid_results
