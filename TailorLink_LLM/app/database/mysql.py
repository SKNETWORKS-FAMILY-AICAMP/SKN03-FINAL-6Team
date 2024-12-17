import pymysql
from app.core.config import settings
from app.core.logger import logger

def get_mysql_connection():
    """
    MySQL 데이터베이스 연결 객체를 반환합니다.

    Returns:
        pymysql.connections.Connection: MySQL 연결 객체
    """

    # MySQL 설정
    db_config = {
        "host": settings.DATABASE_URL,
        "port": 3306,
        "user": settings.DATABASE_USER,
        "password": settings.DATABASE_PASSWORD,
        "database": settings.DATABASE_NAME,
    }

    try:
        # MySQL 연결 생성
        connection = pymysql.connect(**db_config)
        logger.info(f"Connected to MySQL database: {db_config['database']} on {db_config['host']}")
        return connection
    except pymysql.MySQLError as e:
        logger.error(f"MySQL connection failed: {e}")
        raise
