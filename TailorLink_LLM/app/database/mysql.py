from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError
from pymysql import connect, MySQLError
from app.core.config import settings
from app.core.logger import logger

# SQLAlchemy 설정
Base = declarative_base()

# 글로벌 변수로 엔진 및 세션팩토리 초기화
engine = None
Session = None

def create_sqlalchemy_engine():
    """
    SQLAlchemy 엔진을 생성하고 글로벌 변수에 설정.
    """
    global engine, Session
    try:
        connection_string = (
            f"mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}"
            f"@{settings.DATABASE_URL}:3306/{settings.DATABASE_NAME}"
        )
        engine = create_engine(connection_string, pool_pre_ping=True, pool_recycle=1800)
        Session = sessionmaker(bind=engine)
        logger.info("SQLAlchemy engine created successfully.")
    except Exception as e:
        logger.error(f"Failed to create SQLAlchemy engine: {e}")
        raise

def dispose_and_recreate_engine():
    """
    기존 연결 풀을 폐기하고 SQLAlchemy 엔진 및 세션팩토리를 다시 생성.
    """
    global engine
    try:
        logger.info("Disposing the existing SQLAlchemy engine...")
        engine.dispose()  # 기존 연결 풀 폐기
        create_sqlalchemy_engine()  # 새 엔진 및 세션팩토리 생성
        logger.info("SQLAlchemy engine reconnected successfully.")
    except Exception as e:
        logger.error(f"Failed to recreate SQLAlchemy engine: {e}")
        raise

@contextmanager
def get_db_session():
    """
        SQLAlchemy 세션 컨텍스트 매니저
    """
    global Session
    session = Session()
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()
        raise RuntimeError(f"Database error: {e}")
    finally:
        session.close()

# 애플리케이션 시작 시 SQLAlchemy 엔진 초기화
create_sqlalchemy_engine()
