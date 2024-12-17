from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.mysql import get_mysql_connection
from app.database.milvus import get_milvus_client
from app.utils.session_manager import periodic_cleanup, initialize_session, cleanup_sessions
from app.core.logger import logger
from app.core.config import settings
import asyncio

# 글로벌 연결 객체
mysql_connection = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 애플리케이션의 lifespan을 관리합니다.
    """
    global mysql_connection

    # Startup: 데이터베이스 및 세션 관리 초기화
    try:
        logger.info("Starting up...")

        # MySQL 연결 생성
        mysql_connection = get_mysql_connection()
        logger.info("MySQL connection established.")

        # Milvus 연결 생성
        get_milvus_client()
        logger.info("Milvus connection established.")

        # 주기적 세션 정리 작업 시작
        cleanup_task = asyncio.create_task(periodic_cleanup())
        logger.info("Session cleanup task started.")

        yield  # Lifespan 동안 유지되는 작업

    finally:
        # Shutdown: 데이터베이스 및 세션 정리 작업 해제
        logger.info("Shutting down...")

        if mysql_connection:
            mysql_connection.close()
            logger.info("MySQL connection closed.")

        from pymilvus import connections
        connections.disconnect(settings.MILVUS_ALIAS)
        logger.info("Milvus connection closed.")

        # 주기적 세션 정리 작업 취소
        cleanup_task.cancel()
        try:
            await cleanup_task
        except asyncio.CancelledError:
            logger.info("Periodic session cleanup task cancelled.")
