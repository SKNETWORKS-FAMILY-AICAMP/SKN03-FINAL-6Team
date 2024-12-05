#################################
# 테스트를 위한 test 파일(db연결)
#################################

import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4") 

def test_db_connection():
    connection = None
    try:
        # MySQL 연결
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            charset=DB_CHARSET,
            cursorclass=pymysql.cursors.DictCursor
        )

        print("✅ MySQL에 성공적으로 연결되었습니다!")

        # 커서 객체 생성 및 쿼리 실행(쿼리 작성을 위해)
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE();")
            result = cursor.fetchone()
            print("현재 사용 중인 데이터베이스:", result["DATABASE()"])

    except pymysql.MySQLError as e:
        print("❌ MySQL 연결 중 오류 발생:", e)

    finally:
        if connection:
            connection.close()
            print("🔒 MySQL 연결이 종료되었습니다.")

if __name__ == "__main__":
    test_db_connection()
