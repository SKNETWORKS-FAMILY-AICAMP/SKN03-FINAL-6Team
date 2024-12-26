from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.milvus import get_milvus_client
from app.database.mysql import get_db_session
from app.core.logger import logger
from app.core.config import settings
from pymilvus import connections
from sqlalchemy.sql import text
import asyncio

async def monitor_sqlalchemy_connection():
    """
    SQLAlchemy 연결 상태를 주기적으로 확인하고, 문제가 있으면 로그에 기록합니다.
    """
    while True:
        try:
            with get_db_session() as session:
                session.execute(text("SELECT 1"))  # 데이터베이스 연결 확인용 간단한 쿼리
                logger.info("SQLAlchemy connection is healthy.")
        except Exception as e:
            logger.error(f"Error monitoring SQLAlchemy connection: {e}")
        await asyncio.sleep(settings.SQLALCHEMY_CHECK_INTERVAL)  # 주기적 확인 간격

async def monitor_milvus_connection():
    """
    Milvus 연결을 주기적으로 확인하고, 연결이 끊어진 경우 재연결합니다.
    """
    while True:
        try:
            if not connections.has_connection(settings.MILVUS_ALIAS):
                logger.warning("Milvus connection lost. Reconnecting...")
                get_milvus_client()
                logger.info("Milvus reconnected.")
            else:
                logger.info("Milvus connection is healthy.")
        except Exception as e:
            logger.error(f"Error monitoring Milvus connection: {e}")
        await asyncio.sleep(settings.MILVUS_CHECK_INTERVAL)  # 주기적 확인 간격

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 애플리케이션의 lifespan을 관리합니다.
    """

    monitor_milvus_task = None
    monitor_sqlalchemy_task = None

    # Startup: 데이터베이스 및 세션 관리 초기화
    try:
        logger.info("Starting up...")

        # MySQL 연결 생성
        logger.info("MySQL connection established.")
        # SQLAlchemy 연결 상태를 주기적으로 확인하는 작업 시작
        monitor_sqlalchemy_task = asyncio.create_task(monitor_sqlalchemy_connection())

        # Milvus 연결 생성
        get_milvus_client()
        logger.info("Milvus connection established.")
        # Milvus 연결 상태를 주기적으로 확인하는 작업 시작
        monitor_milvus_task = asyncio.create_task(monitor_milvus_connection())

        yield  # Lifespan 동안 유지되는 작업


    finally:
        # Shutdown: 데이터베이스 및 세션 정리 작업 해제
        logger.info("Shutting down...")

        connections.disconnect(settings.MILVUS_ALIAS)
        logger.info("Milvus connection closed.")

        # SQLAlchemy 연결 상태 모니터링 작업 취소
        monitor_sqlalchemy_task.cancel()
        try:
            await monitor_sqlalchemy_task
        except asyncio.CancelledError:
            logger.info("SQLAlchemy monitoring task cancelled.")

        monitor_milvus_task.cancel()
        try:
            await monitor_milvus_task
        except asyncio.CancelledError:
            logger.info("Milvus monitoring task cancelled.")