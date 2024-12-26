from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError
from pymysql import connect, MySQLError
from app.core.config import settings

# SQLAlchemy 설정
Base = declarative_base()

# SQLAlchemy 엔진 및 세션 생성
connection_string = (
    f"mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}"
    f"@{settings.DATABASE_URL}:3306/{settings.DATABASE_NAME}"
)
engine = create_engine(connection_string, pool_pre_ping=True, pool_recycle=1800)
Session = sessionmaker(bind=engine)

# SQLAlchemy 세션 컨텍스트 매니저
@contextmanager
def get_db_session():
    session = Session()
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()
        raise RuntimeError(f"Database error: {e}")
    finally:
        session.close()
