# import torch
from pymilvus.model.hybrid import BGEM3EmbeddingFunction
from langchain.embeddings import Embeddings
from langchain.embeddings.sparse.base import BaseSparseEmbedding
DEVICE = "cpu"

bge_m3_ef = BGEM3EmbeddingFunction(
        model_name='BAAI/bge-m3', # Specify the model name
        device=DEVICE, # Specify the device to use, e.g., 'cpu' or 'cuda:0'
        use_fp16=False # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
    )

bge_m3_def = BGEM3EmbeddingFunction(
        model_name='BAAI/bge-m3', # Specify the model name
        device=DEVICE, # Specify the device to use, e.g., 'cpu' or 'cuda:0'
        use_fp16=False, # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
        return_dense=True,
        rerurn_sparse=False
    )

bge_m3_sef = BGEM3EmbeddingFunction(
        model_name='BAAI/bge-m3', # Specify the model name
        device=DEVICE, # Specify the device to use, e.g., 'cpu' or 'cuda:0'
        use_fp16=False, # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
        return_dense=False,
        rerurn_sparse=True
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
    print("Embeddings:", query_embeddings)
    # Print dimension of dense embeddings
    print("Dense query dim:", bge_m3_ef.dim["dense"], query_embeddings["dense"][0].shape)
    # Since the sparse embeddings are in a 2D csr_array format, we convert them to a list for easier manipulation.
    print("Sparse query dim:", bge_m3_ef.dim["sparse"], list(query_embeddings["sparse"])[0].shape)

    return query_embeddings

def dense_embedding_func():
    return bge_m3_def
def sparse_embedding_func():
    return bge_m3_sef


class BGEM3DenseEmbeddings(Embeddings):
    def __init__(self, model_path: str):
        # embedding_type='dense' 지정
        self.func = BGEM3EmbeddingFunction(model_path=model_path, embedding_type="dense")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # BGEM3EmbeddingFunction 인스턴스는 texts를 입력받아 dense 벡터 리스트 반환한다고 가정
        return self.func(texts)  # [[float, float, ...], [float, ...], ...]

    def embed_query(self, text: str) -> List[float]:
        return self.func([text])[0]

class BGEM3SparseEmbeddings(BaseSparseEmbedding):
    def __init__(self, model_path: str):
        # embedding_type='sparse' 지정
        self.func = BGEM3EmbeddingFunction(model_path=model_path, embedding_type="sparse")

    def embed_documents(self, texts: List[str]) -> List[dict]:
        # BGEM3EmbeddingFunction이 희소벡터를 {"indices": [...], "values": [...]} 형태로 반환한다고 가정
        sparse_vectors = self.func(texts)  # [{"indices": [...], "values": [...]}, ...]
        return sparse_vectors

    def embed_query(self, text: str) -> dict:
        return self.func([text])[0]