import pymysql
import os
from core.ssmparam import get_ssm_parameter

# 환경 변수에서 데이터베이스 연결 정보 가져오기
DB_HOST = os.getenv("MYSQL_URI", '')
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("MYSQL_USER", '')
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", '')
DB_NAME = os.getenv("MYSQL_DB_NAME", '')

def get_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        # database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
        )
    return connection
