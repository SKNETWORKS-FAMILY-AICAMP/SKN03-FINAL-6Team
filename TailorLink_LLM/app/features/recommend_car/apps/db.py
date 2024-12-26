import pymysql
import os
from dotenv import load_dotenv
from app.core.ssmparam import get_ssm_parameter
# .env 파일 로드
# load_dotenv()
import  logging

from app.core.logger import logger

# 환경 변수에서 데이터베이스 연결 정보 가져오기
DB_HOST = get_ssm_parameter('/tailorlink/mysql/MYSQL_URI')
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = get_ssm_parameter('/tailorlink/mysql/MYSQL_USER')
DB_PASSWORD = get_ssm_parameter('/tailorlink/mysql/MYSQL_PASSWORD')
DB_NAME = get_ssm_parameter('/tailorlink/mysql/MYSQL_DB_NAME')

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
