import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import List, Dict
import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# API 키 가져오기
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

def langchain_param():
    return {
        "temperature": 0.9,
        "max_tokens": 500,
        "frequency_penalty": 0.2,
        "presence_penalty": 0.6,
    }

embeddings = OpenAIEmbeddings()

# 문서, pdf 관련해서 여기에 정의할 것 
def load_documents():
    # 예시입니다.
    documents = [
        "제네시스 G80는 고급 세단으로 뛰어난 승차감을 제공합니다.",
        "현대 아반떼는 경제적인 준중형 세단입니다.",
        "기아 쏘렌토는 패밀리 SUV로 인기 있습니다."
    ]
    return documents

def load_pdf():
    return any

# FAISS 인덱스 생성
def create_faiss_index(documents):
    vectors = embeddings.embed_documents(documents)
    dimension = len(vectors[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors))
    return index

# 검색 함수
def search_faiss(index, query, k=5):
    query_vector = embeddings.embed(query)
    D, I = index.search(np.array([query_vector]), k)
    return I[0]

# 문서 리스트에서 인덱스로 문서 가져오기
def get_documents_by_indices(documents, indices):
    return [documents[i] for i in indices]

# 차량 추천 내용인지 판단하는 함수
def is_car_recommendation(search_results):
    return len(search_results) > 0

# 제네시스 차량 여부 판단 함수
def is_genesis(query):
    return '제네시스' in query

class OpenAIClientSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ChatOpenAI(
                model_name="gpt-4",
                **langchain_param()
            )
        return cls._instance

def get_openai_response(messages: List[Dict[str, str]]) -> str:
    client = OpenAIClientSingleton.get_instance()

    # OpenAI 호출 및 응답 생성
    response = client.invoke(messages)
    return response.content
