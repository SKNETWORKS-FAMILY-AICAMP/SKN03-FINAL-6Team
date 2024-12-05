import requests
from bs4 import BeautifulSoup
from .db import get_connection
import logging

logger = logging.getLogger("recommend_car")

def fetch_genesis_models():
    url = 'https://www.genesis.com/kr/ko/main.html'
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"웹 페이지를 가져오는 데 실패했습니다. 상태 코드: {response.status_code}")
        return None

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def extract_model_names(soup):
    model_elements = soup.find_all('strong', class_='vehicle-name')
    model_names = [elem.get_text(strip=True) for elem in model_elements]
    logger.info(f"추출된 모델명: {model_names}")
    return model_names

def is_model_in_db(car_name):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as count FROM car WHERE car_name = %s"
            cursor.execute(sql, (car_name,))
            result = cursor.fetchone()
            return result['count'] > 0
    except Exception as e:
        logger.error(f"DB 오류: {e}")
        return False
    finally:
        connection.close()

def insert_model_into_db(car_name):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO car (car_name) VALUES (%s)"
            cursor.execute(sql, (car_name,))
            new_car_id = cursor.lastrowid
        connection.commit()
        logger.info(f"{car_name}을(를) DB에 추가했습니다. car_id: {new_car_id}")
    except Exception as e:
        connection.rollback()
        logger.error(f"{car_name} 추가 실패: {e}")
    finally:
        connection.close()

def update_car_models():
    logger.info("DB 업데이트 작업이 시작되었습니다.")
    soup = fetch_genesis_models()
    if not soup:
        return

    model_names = extract_model_names(soup)

    for car_name in model_names:
        if is_model_in_db(car_name):
            logger.info(f"{car_name}은(는) 이미 DB에 존재합니다. 스킵합니다.")
        else:
            insert_model_into_db(car_name)
    logger.info("DB 업데이트 작업이 완료되었습니다.")
