import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import List, Dict
import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import os
import requests

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
    ]
    return documents

def load_pdf():
    return any


def schedule_faiss_updates(faiss_index):
    """FAISS 업데이트를 스케줄링."""
    scheduler = BackgroundScheduler()

    # 1시간마다 외부 데이터를 크롤링하여 업데이트
    def update_task():
        for url in external_urls:
            update_faiss_index_with_crawled_data(faiss_index, url)

    scheduler.add_job(update_task, 'interval', hours=1)
    scheduler.start()
    print("FAISS 업데이트 스케줄러가 시작되었습니다.")
def crawl_external_data(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 에러 확인
        soup = BeautifulSoup(response.text, 'html.parser')

        # 모든 <p> 태그의 텍스트를 수집 (필요에 따라 수정 가능)
        data = [p.text.strip() for p in soup.find_all('p') if p.text.strip()]
        return data
    except Exception as e:
        print(f"크롤링 실패: {e}")
        return []

# FAISS 인덱스 생성
def create_faiss_index(documents):
    vectors = embeddings.embed_documents(documents)
    dimension = len(vectors[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors))
    return index

#외부 데이터를 크롤링하여 FAISS 인덱스에 추가.
def update_faiss_index_with_crawled_data(faiss_index, url: str):
    # URL에서 데이터 크롤링
    new_documents = crawl_external_data(url)
    if not new_documents:
        print("크롤링된 데이터가 없습니다.")
        return

    # 새 문서를 벡터화
    new_vectors = embeddings.embed_documents(new_documents)
    faiss_index.add(np.array(new_vectors))  
    print(f"FAISS 인덱스에 {len(new_documents)}개의 새 문서를 추가했습니다.")

# 검색 함수
def search_faiss(index, query, k=5):
    query_vector = embeddings.embed_query(query)
    D, I = index.search(np.array([query_vector]), k)
    return I[0]

# 문서 리스트에서 인덱스로 문서 가져오기
def get_documents_by_indices(documents, indices):
    return [documents[i] for i in indices]


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

# FAISS 초기화 및 외부 데이터 업데이트
documents = load_documents()
faiss_index = create_faiss_index(documents)

# 외부 데이터 여기에 추가
external_urls = [
    
]

for url in external_urls:
    update_faiss_index_with_crawled_data(faiss_index, url)

# 스케줄러 실행
schedule_faiss_updates(faiss_index)