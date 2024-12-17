import os
import logging

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from core.mysql_connctor import get_connection
# load_dotenv()

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

def find_matching_car_id(crawled_car_name):
    """
    크롤링된 car_name에 포함된 RDS의 car_name과 같은 행의 car_id를 반환합니다.
    여러 개가 포함된 경우 가장 먼저 매칭된 값을 반환합니다.
    """
    all_cars = get_all_car_names_and_ids()  # 모든 car_id와 car_name 가져오기
    
    for car in all_cars:  # 순차적으로 검사
        rds_car_id = car['car_id']
        rds_car_name = car['car_name']
        
        # 크롤링된 car_name에 RDS의 car_name이 포함되어 있는지 확인
        if rds_car_name in crawled_car_name:
            return rds_car_id  # 가장 먼저 매칭된 car_id 반환

    # 아무것도 매칭되지 않는 경우
    print(f"'{crawled_car_name}'에 해당하는 RDS car_name을 찾을 수 없습니다.")
    return None
