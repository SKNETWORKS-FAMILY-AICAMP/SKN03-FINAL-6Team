from langchain.tools import tool
from RAG.tools.milvus_search import dense_search, hybrid_search, sparse_search
from RAG.llm.embedding import generate_query_embedding
from RAG.database.milvus_connector import get_collection




def search_milvus(query: str) -> list:
    query_embeddings = generate_query_embedding([query])
    hybrid_results = hybrid_search(
        get_collection('manual'),
        query_embeddings["dense"][0],
        query_embeddings["sparse"]._getrow(0),
        sparse_weight=0.7,
        dense_weight=1.0,
    )
    return hybrid_results
