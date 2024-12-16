from pymilvus import connections, Collection, utility
import os
from common.ssmparam import get_ssm_parameter

MILVUS_URI = get_ssm_parameter('/tailorlink/milvus/MILVUS_URI')
MILVUS_TOKEN = get_ssm_parameter('/tailorlink/milvus/MILVUS_TOKEN')
MILVUS_DB_NAME = 'tailorlink'
MILVUS_ALIAS = 'tailorlink'

def connect_to_milvus():
    """
    Milvus 서버에 연결
    """
    try:
        connections.connect(alias=MILVUS_ALIAS,
                            uri=MILVUS_URI, db_name=MILVUS_DB_NAME,
                            token=MILVUS_TOKEN)

        # connections.connect(alias='default',
        #                     host='192.168.0.130',
        #                     port='19530',
        #                     db_name='tailorlink',)
        print(f"Connected to Milvus-{MILVUS_DB_NAME}")
    except Exception as e:
        print(f"Error connecting to Milvus: {e}")
        raise

def get_collection(collection_name):
    """
    Milvus 컬렉션 가져오기
    """
    if not utility.has_collection(collection_name, using=MILVUS_ALIAS):
        print(f"Collection {collection_name} does not exist.")
        raise ValueError("Please create the collection first.")
    return Collection(collection_name, using=MILVUS_ALIAS)

