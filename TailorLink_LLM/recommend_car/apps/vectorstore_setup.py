# recommend_car/apps/vectorstore_setup.py
import os
import logging
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from .db import get_connection

logger = logging.getLogger("recommend_car")

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

def build_vectorstore():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # 문서형 데이터 추출. 필요에 맞춰 SQL 변경
            sql = """
            SELECT c.car_name, c.car_brand, cdi.fuel, cdi.battery_type, cdi.battery_manufacturer
            FROM car c
            LEFT JOIN car_detail_info cdi ON c.car_id = cdi.car_id
            """
            cursor.execute(sql)
            rows = cursor.fetchall()

            docs = []
            for row in rows:
                doc_text = f"차명: {row['car_name']}, 브랜드: {row['car_brand']}, 연료: {row.get('fuel','')}, 배터리 타입: {row.get('battery_type','')}, 배터리 제조사: {row.get('battery_manufacturer','')}"
                docs.append(doc_text)

            embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
            vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

            vectorstore.add_texts(docs)
            vectorstore.persist()
            logger.info("벡터 스토어 인덱싱 완료")
    except Exception as e:
        logger.error(f"벡터 스토어 구축 중 오류: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    build_vectorstore()
