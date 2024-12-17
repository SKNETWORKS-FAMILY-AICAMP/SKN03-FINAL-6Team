import os
import logging
import re
from difflib import SequenceMatcher
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from recommend_car.apps.db import get_connection
from pymilvus import WeightedRanker, RRFRanker
load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,  
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("chatbot.log"),  
    ],
)
logger = logging.getLogger("recommend_car")

def connect_aws_db():
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT", 3306)
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    
    if not all([db_host, db_port, db_user, db_password, db_name]):
        raise ValueError("데이터베이스 환경 변수를 설정해주세요.")
    
    db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    db = SQLDatabase.from_uri(db_uri)

    return db

def calculate_similarity(a, b):
    """
    두 문자열 사이의 유사도를 계산합니다.
    """
    return SequenceMatcher(None, a, b).ratio()

def extract_detailed_name(base_name, full_name):
    """
    입력된 full_name에서 base_name과 괄호 안의 세부 정보만 추출합니다.
    예: "G80 (RG3) 가솔린 3.5L" → "G80 (RG3)"
    """
    pattern = re.escape(base_name) + r"\s*(\([^)]*\))"
    match = re.search(pattern, full_name)
    if match:
        return f"{base_name} {match.group(1).strip()}"  # base_name + 세부 정보 반환
    return None

def get_car_id_by_name(car_name):
    """
    car_name에 해당하는 car_id를 데이터베이스에서 조회합니다.
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT car_id FROM car WHERE car_name = %s"
            cursor.execute(sql, (car_name,))
            result = cursor.fetchone()
            print("검색 결과: " + result)
            if result:
                return result['car_id']
            else:
                return 0  # car_name이 없을 경우
    except Exception as e:
        print(f"Error fetching car_id for {car_name}: {e}")
        return None
    finally:
        connection.close()
    
def get_all_car_names_and_ids():
    """
    RDS에서 모든 car_name과 car_id를 가져옵니다.
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT car_id, car_name FROM car"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result  # car_id와 car_name 리스트 반환
    except Exception as e:
        print(f"Error fetching car names and IDs: {e}")
        return []
    finally:
        connection.close()

def add_car_name_to_db(car_name):
    """
    car_name이 DB에 없을 경우 이름만 추가하고, 새로운 car_id를 반환합니다.
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # car_name을 삽입
            sql_insert = "INSERT INTO car (car_name) VALUES (%s)"
            cursor.execute(sql_insert, (car_name,))
            connection.commit()
            
            # 방금 삽입된 car_id를 가져옴
            sql_select = "SELECT LAST_INSERT_ID() as car_id"
            cursor.execute(sql_select)
            result = cursor.fetchone()
            if result:
                return result['car_id']
            return None
    except Exception as e:
        print(f"Error adding car_name '{car_name}' to DB: {e}")
        return None
    finally:
        connection.close()

def find_matching_car_id(crawled_car_name):
    """
    정확 일치를 우선 검사하고, 세부 모델명을 추출해 DB에 추가합니다.
    대소문자를 구분하지 않고 car_name을 검사합니다.
    """
    all_cars = get_all_car_names_and_ids()  # 모든 car_id와 car_name 가져오기

    # 입력된 car_name을 소문자로 변환
    crawled_car_name_lower = crawled_car_name.lower()

    # 1. 정확한 일치 확인 (대소문자 무시)
    for car in all_cars:
        rds_car_id = car['car_id']
        rds_car_name_lower = car['car_name'].lower()
        if rds_car_name_lower == crawled_car_name_lower:
            print(f"정확히 일치하는 차량명을 찾았습니다: {car['car_name']} → car_id={rds_car_id}")
            return rds_car_id

    # 2. 일반 모델명 확인 및 세부 모델명 추가
    for car in all_cars:
        rds_car_id = car['car_id']
        rds_car_name = car['car_name']

        if rds_car_name in crawled_car_name:
            detailed_name = extract_detailed_name(rds_car_name, crawled_car_name)
            if detailed_name and detailed_name != rds_car_name:
                new_car_name = detailed_name
                print(f"세부 모델명 '{new_car_name}'을 DB에 추가합니다...")
                new_car_id = add_car_name_to_db(new_car_name)
                if new_car_id:
                    print(f"'{new_car_name}'이 DB에 추가되었습니다. 새 car_id: {new_car_id}")
                    return new_car_id
            print(f"기존 모델명 '{rds_car_name}'이 매칭되었습니다 → car_id={rds_car_id}")
            return rds_car_id

    # 3. 매칭되는 모델명이 없으면 전체 이름 추가
    print(f"'{crawled_car_name}'에 해당하는 차량명이 없습니다. DB에 추가합니다...")
    new_car_id = add_car_name_to_db(crawled_car_name)
    if new_car_id:
        print(f"'{crawled_car_name}'이 DB에 추가되었습니다. 새 car_id: {new_car_id}")
        return new_car_id
    else:
        print("DB에 car_name을 추가하는 데 실패했습니다.")
        return None

def rerank_results(db_results, milvus_results, strategy="weighted", weights=None):
    """
    DB 결과와 Milvus 결과를 Re-rank하여 최종 리스트를 반환합니다.
    :param db_results: SQL DB에서 가져온 결과 리스트
    :param milvus_results: Milvus에서 가져온 벡터 검색 결과 리스트
    :param strategy: "weighted" 또는 "rrf" 선택
    :param weights: WeightedRanker에 사용할 가중치 리스트
    """
    if strategy == "weighted":
        if not weights:
            weights = [0.7, 0.3]  # 기본 가중치 설정

        # WeightedRanker 설정
        reranker = WeightedRanker(*weights)

        # Milvus 결과의 점수를 추출
        scores = [result['distance'] for result in milvus_results]
        reranked_results = reranker.rerank(
            routes=[
                {"id": result['id'], "score": score}
                for result, score in zip(milvus_results, scores)
            ]
        )
    elif strategy == "rrf":
        # RRFRanker 설정
        reranker = RRFRanker()
        reranked_results = reranker.rerank(
            routes=[
                {"id": result['id'], "rank": idx + 1}
                for idx, result in enumerate(milvus_results)
            ]
        )
    else:
        raise ValueError("지원되지 않는 re-ranking 전략입니다.")

    # Re-ranked ID와 DB 결과 매칭
    final_results = []
    for rerank_result in reranked_results:
        for db_result in db_results:
            if rerank_result['id'] == db_result['id']:
                final_results.append({**db_result, "score": rerank_result['score']})
                break

    # 점수 기준으로 정렬
    final_results.sort(key=lambda x: x['score'], reverse=True)
    return final_results
