from pymilvus import MilvusClient
from recommend_car.apps.ssmparam import get_ssm_parameter

# Milvus 연결 정보
MILVUS_URI = get_ssm_parameter('/tailorlink/milvus/MILVUS_URI')
MILVUS_TOKEN = get_ssm_parameter('/tailorlink/milvus/MILVUS_TOKEN')
MILVUS_DB_NAME = 'tailorlink'

# MilvusClient 생성
client = MilvusClient(uri=MILVUS_URI, token=MILVUS_TOKEN)

def create_milvus_collection(collection_name):
    """
    Milvus 컬렉션 생성 (Dynamic Field 활성화)
    """
    try:
        if client.has_collection(collection_name):
            print(f"기존 컬렉션 '{collection_name}' 삭제 중...")
            client.drop_collection(collection_name)

        client.create_collection(
            collection_name=collection_name,
            dimension=768,  # 벡터 차원
            primary_field="id",
            enable_dynamic_field=True  # Dynamic Field 활성화
        )
        print(f"컬렉션 '{collection_name}'이 생성되었습니다.")
    except Exception as e:
        print(f"Error creating collection: {e}")
        raise
    
def insert_initial_data(collection_name, car_id, embedding, metadata):
    """
    Milvus에 초기 데이터 삽입 (Dynamic Fields 포함)
    """
    try:
        data = [{
            "car_id": car_id,
            "embedding": embedding,
            **metadata  # 동적 필드 추가
        }]
        client.insert(collection_name=collection_name, data=data)
        print(f"초기 데이터가 컬렉션 '{collection_name}'에 삽입되었습니다. car_id: {car_id}")
    except Exception as e:
        print(f"Error inserting initial data into Milvus: {e}")
        raise

def update_dynamic_fields(collection_name, search_condition, new_dynamic_fields):
    """
    Dynamic Fields를 업데이트 (기존 레코드 삭제 후 재삽입)
    """
    try:
        # 기존 레코드 조회
        results = client.query(
            collection_name=collection_name,
            expr=search_condition,
            output_fields=["*"]  # 모든 필드 반환
        )
        if not results:
            print("조건에 맞는 레코드가 없습니다.")
            return

        # 기존 데이터 확장
        for record in results:
            updated_record = {
                "car_id": record["car_id"],
                "embedding": record["embedding"],
                **record.get("$meta", {}),  # 기존 Dynamic Field 복사
                **new_dynamic_fields       # 추가할 Dynamic Field
            }
            # 기존 레코드 삭제
            client.delete(collection_name=collection_name, expr=search_condition)

            # 새로운 레코드 삽입
            client.insert(collection_name=collection_name, data=[updated_record])
            print(f"레코드 업데이트 완료: {updated_record}")
    except Exception as e:
        print(f"Dynamic Field 업데이트 중 오류 발생: {e}")
        raise

def search_in_milvus(collection_name, query_embedding, top_k=5):
    """
    Milvus에서 유사도 검색 수행
    """
    try:
        results = client.search(
            collection_name=collection_name,
            data=[query_embedding],
            limit=top_k,
            anns_field="vector",
            output_fields=["*"]  # 모든 필드 반환
        )
        for hits in results:
            for hit in hits:
                print(f"ID: {hit['id']}, Fields: {hit}")
        return results
    except Exception as e:
        print(f"Error searching in Milvus: {e}")
        raise
