import os
import logging
import re
import json
import re
from difflib import SequenceMatcher
from langchain_community.utilities import SQLDatabase
from app.features.recommend_car.apps.db import get_connection
from app.core.config import settings


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
    db_host = settings.DATABASE_URL
    db_port = "3306"
    db_user = settings.DATABASE_USER
    db_password = settings.DATABASE_PASSWORD
    db_name = settings.DATABASE_NAME
    
    if not all([db_host, db_port, db_user, db_password, db_name]):
        raise ValueError("데이터베이스 환경 변수를 설정해주세요.")

    db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    logger.info(db_uri)
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

def parse_milvus_results(search_results):
    """
    Milvus 검색 결과를 파싱하여 사용할 수 있는 형태로 변환합니다.
    """
    try:
        # 검색 결과를 문자열로 출력 (디버깅용)
        print("[Debug 확인] " + str(search_results))

        parsed_results = []
        for result_list in search_results:
            for hit in result_list:
                metadata = hit.get("entity")
                car_id = metadata.get("car_id")

                # 유효성 검증: car_id와 metadata가 None이면 추가하지 않음
                if car_id is not None or metadata is not None:
                    parsed_results.append({
                        "car_id": car_id,
                        "metadata": metadata
                    })

        # 결과가 비어 있는 경우 디버깅 메시지 출력
        if not parsed_results:
            print("[DEBUG] Milvus 검색 결과가 유효하지 않습니다. 모든 항목이 None입니다.")
    except Exception as e:
        print(f"[ERROR] Milvus 결과 파싱 중 오류 발생: {e}")
        parsed_results = []

    print("[DEBUG] Milvus 파싱 결과:", parsed_results)
    return parsed_results

def extract_json_from_text(raw_text):
    """
    주어진 텍스트에서 JSON 형식의 데이터를 추출하고 Python 딕셔너리로 반환
    """
    try:
        # 백틱 안에 있는 JSON 배열 추출
        json_pattern = re.compile(r'```json\n(.*?)\n```', re.DOTALL)
        json_match = json_pattern.search(raw_text)
        if json_match:
            json_data = json_match.group(1)  # 매칭된 JSON 문자열
            # JSON 문자열을 Python 딕셔너리로 변환
            return json.loads(json_data)
        else:
            print("[ERROR] JSON 형식 데이터를 찾을 수 없습니다.")
            return None
    except Exception as e:
        print(f"[ERROR] JSON 추출 중 오류 발생: {e}")
        return None