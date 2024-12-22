# import torch
from pymilvus.model.hybrid import BGEM3EmbeddingFunction
DEVICE = "cpu"

bge_m3_ef = BGEM3EmbeddingFunction(
        model_name='BAAI/bge-m3', # Specify the model name
        device=DEVICE, # Specify the device to use, e.g., 'cpu' or 'cuda:0'
        use_fp16=False # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
    )

def get_document_embedding_dim():
    docs_embeddings = bge_m3_ef.encode_documents(['Hi'])
    return bge_m3_ef.dim["dense"]

def generate_document_embeddings(docs:list):
    """
    문서 리스트를 입력받아 임베딩을 생성합니다.

    Args:
        docs (list): 문서 텍스트 리스트.

    Returns:
        dict: {"dense": Dense 임베딩 리스트, "sparse": Sparse 임베딩 리스트}
    """

    docs_embeddings = bge_m3_ef.encode_documents(docs)

    # Print embeddings
    # print("Embeddings:", docs_embeddings)
    # # Print dimension of dense embeddings
    # print("Dense document dim:", bge_m3_ef.dim["dense"], docs_embeddings["dense"][0].shape)
    # print("Sparse document dim:", bge_m3_ef.dim["sparse"], list(docs_embeddings["sparse"])[0].shape)

    return docs_embeddings

def generate_query_embeddings(queries:list):
    """
    쿼리 리스트를 입력받아 임베딩을 생성합니다.

    Args:
        queries (list): 쿼리 텍스트 리스트.

    Returns:
        dict: {"dense": Dense 임베딩 리스트, "sparse": Sparse 임베딩 리스트}
    """

    query_embeddings = bge_m3_ef.encode_queries(queries)

    # Print embeddings
    # print("Embeddings:", query_embeddings)
    # # Print dimension of dense embeddings
    # print("Dense query dim:", bge_m3_ef.dim["dense"], query_embeddings["dense"][0].shape)
    # # Since the sparse embeddings are in a 2D csr_array format, we convert them to a list for easier manipulation.
    # print("Sparse query dim:", bge_m3_ef.dim["sparse"], list(query_embeddings["sparse"])[0].shape)

    return query_embeddings
