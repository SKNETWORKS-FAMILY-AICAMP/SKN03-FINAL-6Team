from pymilvus import connections, Collection, utility
import os

MILVUS_HOST = os.getenv("MILVUS_HOST", "http://192.168.0.130")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")

def connect_to_milvus():
    """
    Milvus 서버에 연결
    """
    try:
        connections.connect(alias="default", host="192.168.0.130", port="19530", db_name='tailorlink')
        print("Connected to Milvus")
    except Exception as e:
        print(f"Error connecting to Milvus: {e}")
        raise

def get_collection(collection_name):
    """
    Milvus 컬렉션 가져오기
    """
    connect_to_milvus()
    if not utility.has_collection(collection_name):
        print(f"Collection {collection_name} does not exist.")
        raise ValueError("Please create the collection first.")
    return Collection(collection_name)

