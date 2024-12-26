from pymilvus import connections, utility, Collection
from app.core.config import settings
from app.core.logger import logger

def get_milvus_client():
    """
    Milvus 클라이언트를 초기화하고 반환합니다.

    Returns:
        pymilvus.client.Client: Milvus 클라이언트
    """
    try:
        # Milvus 연결 생성
        connections.connect(
            alias=settings.MILVUS_ALIAS,
            uri=settings.MILVUS_URI,
            db_name=settings.MILVUS_DB_NAME,
            token=settings.MILVUS_TOKEN
        )
        logger.info(f"Connected to Milvus at {settings.MILVUS_URI}")
    except Exception as e:
        logger.error(f"Milvus connection failed: {e}")
        raise

def get_collection(collection_name):
    """
    Milvus 컬렉션 가져오기
    """
    if not utility.has_collection(collection_name, using=settings.MILVUS_ALIAS):
        print(f"Collection {collection_name} does not exist.")
        raise ValueError("Please create the collection first.")
    return Collection(collection_name, using=settings.MILVUS_ALIAS)