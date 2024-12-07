# import os
# from langchain_openai import OpenAIEmbeddings
# from langchain_chroma import Chroma

# openai_api_key = os.getenv("OPENAI_API_KEY")
# embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
# vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

# def search_documents(query: str, k: int = 3):
#     docs = vectorstore.similarity_search(query, k=k)
#     return [doc.page_content for doc in docs]
# recommend_car/apps/retrieval.py
import os
from .utils import embedding_function
# langchain_chroma로 import 경로 변경 필요 시:
from langchain_chroma import Chroma

# 벡터 스토어 초기화
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_function
)

def search_documents(query: str, k: int = 3):
    docs = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]
