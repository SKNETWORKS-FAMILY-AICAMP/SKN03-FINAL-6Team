import os
import faiss
import numpy as np
import requests
from dotenv import load_dotenv
from typing import List, Dict
import hashlib
import time
from cachetools import TTLCache, cached
from cachetools.keys import hashkey
from threading import Semaphore
import asyncio
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

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

# OpenAI Embeddings 초기화
embeddings = OpenAIEmbeddings()

# 해시 기반 중복 데이터 확인을 위한 저장소
document_store = set()

# API 키 및 검색 엔진 ID 가져오기
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

if not GOOGLE_API_KEY or not GOOGLE_CSE_ID or not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
    raise ValueError("Google 및 Naver API 키가 설정되지 않았습니다.")

# 요청 수 제한을 위한 세마포어
rate_limit = Semaphore(1)
REQUEST_INTERVAL = 1 

# 검색 결과 캐싱 (5분 TTL)
search_cache = TTLCache(maxsize=100, ttl=300)

# OpenAI 응답 캐싱 (10분 TTL)
openai_cache = TTLCache(maxsize=100, ttl=600)

# 빈 FAISS 인덱스 생성 함수
def create_empty_faiss_index(dimension: int) -> faiss.IndexFlatL2:
    index = faiss.IndexFlatL2(dimension)
    return index

# 텍스트를 일정 크기로 분할
def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# 중복 문서 확인
def is_duplicate_document(document: str) -> bool:
    document_hash = hashlib.sha256(document.encode()).hexdigest()
    if document_hash in document_store:
        return True
    document_store.add(document_hash)
    return False

# Google 검색 함수
@cached(search_cache, key=lambda query, num_results: hashkey(query))
def google_search(query: str, num_results: int = 5) -> List[str]:
    with rate_limit:
        time.sleep(REQUEST_INTERVAL)
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CSE_ID,
            "q": query,
            "num": num_results,
        }
        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            results = response.json().get("items", [])
            snippets = [item["snippet"] for item in results]
            return snippets
        except Exception as e:
            print(f"Google 검색 실패: {e}")
            return []

# Naver 검색 함수
@cached(search_cache, key=lambda query, num_results: hashkey(query))
def naver_search(query: str, num_results: int = 5) -> List[str]:
    with rate_limit:
        time.sleep(REQUEST_INTERVAL)
        search_url = "https://openapi.naver.com/v1/search/news.json"
        headers = {
            "X-Naver-Client-Id": NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        }
        params = {
            "query": query,
            "display": num_results,
        }
        try:
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            results = response.json().get("items", [])
            snippets = [item["description"].replace('<b>', '').replace('</b>', '') for item in results]
            return snippets
        except Exception as e:
            print(f"Naver 검색 실패: {e}")
            return []

# 외부 데이터 수집 함수
def collect_external_data(query: str) -> List[str]:
    google_results = google_search(query)
    naver_results = naver_search(query)
    combined_results = google_results + naver_results
    return combined_results

# 비동기적으로 외부 데이터 처리
async def update_faiss_with_external_data(faiss_index: faiss.IndexFlatL2, query: str, documents_list: List[str]) -> dict:
    loop = asyncio.get_event_loop()
    # 외부 데이터 수집
    documents = await loop.run_in_executor(None, collect_external_data, query)
    if not documents:
        return {"message": "외부 데이터에서 결과를 찾을 수 없습니다.", "status": "failure"}

    # 문서 분할 및 중복 제거
    all_chunks = []
    for doc in documents:
        chunks = split_text(doc)
        unique_chunks = [chunk for chunk in chunks if not is_duplicate_document(chunk)]
        all_chunks.extend(unique_chunks)

    if not all_chunks:
        return {"message": "새로운 문서가 없습니다.", "status": "failure"}

    # 임베딩 벡터 생성 및 FAISS 인덱스에 추가
    vectors = embeddings.embed_documents(all_chunks)
    faiss_index.add(np.array(vectors))
    documents_list.extend(all_chunks)
    print(f"FAISS 인덱스 업데이트: {len(all_chunks)}개의 문서 추가.")
    return {"message": f"FAISS 인덱스에 {len(all_chunks)}개의 문서를 추가했습니다.", "status": "success"}

# FAISS 검색
def search_faiss(index: faiss.IndexFlatL2, query: str, k: int = 3) -> List[int]:
    query_vector = embeddings.embed_query(query)
    D, I = index.search(np.array([query_vector]), k)
    return I[0]

# 인덱스로부터 문서 가져오기
def get_documents_by_indices(documents: List[str], indices: List[int]) -> List[str]:
    return [documents[i] for i in indices if i < len(documents)]

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

# OpenAI 응답 캐싱
@cached(openai_cache, key=lambda messages: hashkey(tuple((msg['role'], msg['content']) for msg in messages)))
def get_openai_response(messages: List[Dict[str, str]]) -> str:
    client = OpenAIClientSingleton.get_instance()
    response = client.invoke(messages)
    return response.content
