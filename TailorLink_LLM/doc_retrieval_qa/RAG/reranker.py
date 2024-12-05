
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

def get_reranker(retriever, model_name="BAAI/bge-reranker-v2-m3", top_n=5):
    # 모델 초기화
    model = HuggingFaceCrossEncoder(model_name=model_name)
    # 상위 3개의 문서 선택
    compressor = CrossEncoderReranker(model=model, top_n=top_n)

    # 문서 압축 검색기 초기화
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )