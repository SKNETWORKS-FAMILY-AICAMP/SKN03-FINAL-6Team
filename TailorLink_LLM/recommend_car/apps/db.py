import pymysql
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 데이터베이스 연결 정보 가져오기
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

def get_car_info(query):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            # 차량 정보 검색 쿼리
            sql = """
            SELECT model_id, name, description, image_url
            FROM car_models
            WHERE name LIKE %s OR description LIKE %s
            """
            cursor.execute(sql, (f"%{query}%", f"%{query}%"))
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as e:
        print("❌ 데이터베이스 오류:", e)
    finally:
        if connection:
            connection.close()
