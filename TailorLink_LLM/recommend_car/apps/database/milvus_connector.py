from pymilvus import connections, Collection, utility, FieldSchema, CollectionSchema, DataType, MilvusClient
from transformers import AutoModel, AutoTokenizer
from recommend_car.apps.ssmparam import get_ssm_parameter
from recommend_car.apps.utils import find_matching_car_id
import torch

# Milvus 연결 정보
MILVUS_URI = get_ssm_parameter('/tailorlink/milvus/MILVUS_URI')
MILVUS_TOKEN = get_ssm_parameter('/tailorlink/milvus/MILVUS_TOKEN')
MILVUS_DB_NAME = 'tailorlink'
MILVUS_ALIAS = 'tailorlink'

# KoBERT 모델 초기화
model = AutoModel.from_pretrained("monologg/kobert")
tokenizer = AutoTokenizer.from_pretrained("monologg/kobert", trust_remote_code=True)

def connect_to_milvus():
    """
    Milvus 서버 연결
    """
    try:
        print(f"Connecting to Milvus at {MILVUS_URI}")
        connections.connect(
            alias=MILVUS_ALIAS,
            uri=MILVUS_URI,
            db_name=MILVUS_DB_NAME,
            token=MILVUS_TOKEN
        )
        print(f"Connected to Milvus database: {MILVUS_DB_NAME}")
    except Exception as e:
        print(f"Error connecting to Milvus: {e}")
        raise


def create_milvus_collection(collection_name):
    """
    Milvus 컬렉션 생성 (Dynamic Field 활성화)
    """
    try:
        if utility.has_collection(collection_name, using=MILVUS_ALIAS):
            Collection(collection_name).drop()

        fields = [
            FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=True, max_length=100),
            FieldSchema(name="car_id", dtype=DataType.INT32),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
        ]
        schema = CollectionSchema(fields, dimentions=4, description="Dynamic Field enabled collection", enable_dynamic_field=True)
        Collection(name=collection_name, schema=schema, using=MILVUS_ALIAS)
        print(f"Collection '{collection_name}' created with Dynamic Field enabled.")
    except Exception as e:
        print(f"Error creating collection: {e}")
        raise


def create_index(collection_name):
    """
    Milvus 인덱스 생성
    """
    try:
        collection = Collection(collection_name, using=MILVUS_ALIAS)
        index_params = {
            "index_type": "IVF_FLAT",  # 효율적인 검색을 위한 기본 인덱스
            "metric_type": "L2",
            "params": {"nlist": 128}
        }
        collection.create_index(field_name="embedding", index_params=index_params)
        print(f"Index created for collection '{collection_name}'")
    except Exception as e:
        print(f"Error creating index: {e}")
        raise


def load_collection(collection_name):
    """
    컬렉션 메모리 로드
    """
    try:
        collection = Collection(collection_name, using=MILVUS_ALIAS)
        collection.load()
        print(f"Collection '{collection_name}' is loaded into memory.")
    except Exception as e:
        print(f"Error loading collection: {e}")
        raise


def save_to_milvus(collection_name, embedding, metadata):
    """
    Milvus에 데이터 저장 (Dynamic Field 사용)
    """
    try:
        collection = Collection(collection_name, using=MILVUS_ALIAS)
        car_id = find_matching_car_id(metadata.get("car_name", ""))
        if not car_id:
            print(f"'{metadata.get("car_name", "")}'에 해당하는 car_id를 찾을 수 없습니다. 저장을 건너뜁니다.")
            return
        # 데이터 삽입
        entities = [    
            [car_id],
            [embedding],
            [{"car_name": metadata.get("car_name", ""),
            "car_info": metadata.get("car_info", ""),
            "keywords": metadata.get("keywords", {}),
            "page": metadata.get("page", 0)}]
        ]   
        
        # Dynamic Field 데이터 삽입
        if metadata:
            collection.insert(entities)
            print(f"Data stored in Milvus collection '{collection_name}' with metadata: {metadata}")
        else:
            collection.insert(entities)
            print(f"Data stored in Milvus collection '{collection_name}' without metadata.")
    except Exception as e:
        print(f"Error saving to Milvus: {e}")
        raise

def search_in_milvus(collection_name, query_text, top_k=5):
    """
    Milvus에서 검색 (Dynamic Field 포함)
    """
    try:
        collection = Collection(collection_name, using=MILVUS_ALIAS)

        # 검색할 텍스트 임베딩 생성
        inputs = tokenizer(
            query_text, return_tensors="pt", padding=True, truncation=True, max_length=tokenizer.model_max_length
        )
        with torch.no_grad():
            outputs = model(**inputs)
        query_embedding = outputs.last_hidden_state[:, 0, :].squeeze(0).tolist()

        # 검색 실행
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k
        )

        # 결과 출력
        for hits in results:
            for hit in hits:
                print(f"ID: {hit.id}, Metadata: {hit.entity}")
        return results
    except Exception as e:
        print(f"Error searching in Milvus: {e}")
        raise
