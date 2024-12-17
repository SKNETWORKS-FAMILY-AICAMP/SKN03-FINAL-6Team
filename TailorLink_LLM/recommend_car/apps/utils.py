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

def rerank_results(db_results, milvus_results, weights=[0.6, 0.4]):
    """
    DB와 Milvus 검색 결과를 Re-ranking 하는 함수.
    """
    try:
        combined_results = []

        # DB 결과 추가
        for result in db_results:
            combined_results.append({
                "car_id": result.get("car_id", "unknown"),
                "car_name": result.get("car_name", "알 수 없는 차량"),
                "score": weights[0] * 1.0  # 기본 점수 (DB)
            })

        # Milvus 결과 추가
        for result in milvus_results:
            combined_results.append({
                "car_id": result.get("car_id", "unknown"),
                "car_name": result.get("car_name", "알 수 없는 차량"),
                "score": weights[1] * (100.0 - result.get("score", 100.0))  # 거리 반전 점수
            })

        # 점수를 기준으로 정렬
        reranked_results = sorted(combined_results, key=lambda x: x["score"], reverse=True)
        print("Re-ranking 결과:", reranked_results)
        return reranked_results

    except Exception as e:
        print(f"[ERROR] Re-ranking 중 오류 발생: {e}")
        return [{"car_id": "unknown", "car_name": "알 수 없는 차량", "score": 0.0}]

def parse_milvus_results(search_results):
    """
    Milvus 검색 결과를 파싱하여 사용할 수 있는 형태로 변환합니다.
    """
    parsed_results = []
    try:
        for hit in search_results:
            if isinstance(hit, dict):
                parsed_results.append({
                    "car_id": hit.get("id", "unknown"),
                    "car_name": "알 수 없는 차량",
                    "score": hit.get("distance", 100.0)  # 거리 기반 점수
                })
    except Exception as e:
        print(f"[ERROR] Milvus 결과 파싱 중 오류 발생: {e}")

    if not parsed_results:
        print("Milvus 결과가 비어 있습니다. 기본값으로 설정합니다.")
        parsed_results = [{"car_id": "unknown", "car_name": "알 수 없는 차량", "score": 100.0}]

    print("파싱된 Milvus 결과:", parsed_results)
    return parsed_results