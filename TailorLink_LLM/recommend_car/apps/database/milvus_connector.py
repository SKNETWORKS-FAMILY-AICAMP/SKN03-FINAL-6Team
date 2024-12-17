import torch
from transformers import AutoModel, AutoTokenizer
from pymilvus import MilvusClient, DataType
from recommend_car.apps.ssmparam import get_ssm_parameter

# Milvus 설정
MILVUS_URI = get_ssm_parameter('/tailorlink/milvus/MILVUS_URI')
MILVUS_TOKEN = get_ssm_parameter('/tailorlink/milvus/MILVUS_TOKEN')
MILVUS_DB_NAME = 'tailorlink'
# Milvus 클라이언트 초기화
client = MilvusClient(uri=MILVUS_URI, token=MILVUS_TOKEN, db_name="tailorlink")

# KoBERT 모델 및 토크나이저 초기화
model = AutoModel.from_pretrained("monologg/kobert")
tokenizer = AutoTokenizer.from_pretrained("monologg/kobert", trust_remote_code=True)

def generate_kobert_embedding(text):
    """
    KoBERT를 사용해 텍스트 임베딩 생성
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = outputs.last_hidden_state[:, 0, :].squeeze(0).tolist()
    if len(embedding) != 768:
        raise ValueError(f"임베딩 차원이 768이 아닙니다. 현재 차원: {len(embedding)}")
    print(f"임베딩 생성 완료: 길이 {len(embedding)}")  # 디버깅용 출력
    return embedding

def create_milvus_collection(collection_name):
    """
    Milvus 컬렉션 생성 및 필드별 인덱스 추가
    """
    try:
        print(f"컬렉션 '{collection_name}' 생성 중...")

        # 기존 컬렉션 삭제
        if client.has_collection(collection_name):
            print(f"기존 컬렉션 '{collection_name}' 삭제 중...")
            client.drop_collection(collection_name)

        # 스키마 생성
        schema = client.create_schema(auto_id=True, enable_dynamic_field=True)
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)  # Primary Key
        schema.add_field(field_name="car_id", datatype=DataType.INT32)
        schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=768)

        index_params = client.prepare_index_params()
        # car_id에 정렬 인덱스 (STL_SORT)
        index_params.add_index(
            collection_name=collection_name,
            field_name="car_id",
            index_type="STL_SORT"
        )

        # vector 필드에 벡터 인덱스 (AUTOINDEX)
        index_params.add_index(
            collection_name=collection_name,
            field_name="vector",
            index_type="AUTOINDEX",
            metric_type="L2"  # 거리 계산 방식
        )

        # 컬렉션 생성
        client.create_collection(collection_name=collection_name, schema=schema, index_params=index_params)
        print(f"컬렉션 '{collection_name}'이 생성되었습니다.")

        # 컬렉션 로드
        client.load_collection(collection_name=collection_name)
        print(f"컬렉션 '{collection_name}'이 메모리에 로드되었습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")
        raise

def insert_or_update_data(collection_name, car_id, embedding, metadata):
    """
    car_id가 존재하면 동적 필드 업데이트, 없으면 새로운 데이터 삽입
    """
    if not embedding or not isinstance(embedding, list) or len(embedding) != 768:
        raise ValueError("임베딩 데이터가 비어있거나 차원이 올바르지 않습니다.")

    # 컬렉션 로드
    print(f"컬렉션 '{collection_name}'을 메모리에 로드 중...")
    client.load_collection(collection_name=collection_name)
    print(f"컬렉션 '{collection_name}'이 메모리에 로드되었습니다.")

    search_condition = f"car_id == {car_id}"
    results = client.query(
        collection_name=collection_name, 
        filter=search_condition,  # expr 대신 filter 사용
        output_fields=["car_id", "vector", "$meta"]  # 원하는 필드 명확히 지정
    )

    if results:
        # 동적 필드 업데이트
        updated_record = {
            "car_id": results[0]["car_id"],
            "vector": results[0]["vector"],
            **results[0].get("$meta", {}),
            **metadata  # 새 동적 필드 추가
        }
        client.delete(collection_name=collection_name, filter=search_condition)
        client.insert(collection_name=collection_name, data=[updated_record])
        print(f"car_id '{car_id}'의 동적 필드가 업데이트되었습니다.")
    else:
        # 새 데이터 삽입
        data = [{
            "car_id": car_id,
            "vector": embedding,
            **metadata
        }]
        client.insert(collection_name=collection_name, data=data)
        print(f"새로운 데이터가 삽입되었습니다. car_id: {car_id}")

def insert_data_incrementally(collection_name, car_id, embedding, metadata):
    """
    Milvus 컬렉션에 데이터를 동적으로 삽입 (기존 데이터 유지)
    """
    if not embedding or not isinstance(embedding, list) or len(embedding) != 768:
        raise ValueError("임베딩 데이터가 비어있거나 차원이 올바르지 않습니다.")

    try:
        # 컬렉션 로드
        print(f"컬렉션 '{collection_name}'을 메모리에 로드 중...")
        client.load_collection(collection_name=collection_name)
        print(f"컬렉션 '{collection_name}'이 메모리에 로드되었습니다.")

        # 새로운 데이터 준비
        new_data = [{
            "car_id": car_id,
            "vector": embedding,
            **metadata  # 동적 필드 추가
        }]

        # 데이터 삽입
        client.insert(collection_name=collection_name, data=new_data)
        print(f"새로운 데이터가 추가되었습니다: car_id={car_id}")

    except Exception as e:
        print(f"데이터 삽입 중 오류 발생: {e}")
        raise
