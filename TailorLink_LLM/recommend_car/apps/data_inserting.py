import sys
import os
import json
import asyncio
import gradio as gr
import pyperclip
import torch
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai.chunking_strategy import RegexChunking
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from transformers import AutoModel, AutoTokenizer
from recommend_car.apps.database.milvus_connector import (
    client,
    create_milvus_collection,
    insert_or_update_data
)
from recommend_car.apps.utils import find_matching_car_id

load_dotenv()

# KoBERT 모델 및 토크나이저 초기화
model = AutoModel.from_pretrained("monologg/kobert")
tokenizer = AutoTokenizer.from_pretrained("monologg/kobert", trust_remote_code=True)

# 제네시스 차량 정보를 저장할 데이터 모델 정의
class GenesisCarInfo(BaseModel):
    car_name: str = Field(..., description="차량명")
    car_image: str = Field(..., description="차량 이미지 url")
    car_info: str = Field(..., description="차량 정보")
    car_review: str = Field(..., description="차량 리뷰")
    keywords: list = Field(..., description="페이지에 할당된 키워드 목록")

# 추출 전략 설정
extraction_strategy = LLMExtractionStrategy(
    provider="openai/gpt-4o-mini",
    api_key=os.getenv('OPENAI_API_KEY'),
    schema=GenesisCarInfo.model_json_schema(),
    extraction_type="schema",
    apply_chunking=False,
    instruction=(
        """
        크롤링한 내용을 다음 세부 정보로 정리하고, 한국어로 번역하여 Markdown 형식으로 작성하세요.
        리뷰 내용을 최대한 자세하게 작성하고, 사용자의 실제 경험과 의견을 포함한 풍부한 내용을 제공하세요.

        ### 차량명
        차량명 내용을 간결하게 작성하세요.
        
        ### 차량이미지
        차량 이미지 url을 받아오세요.

        ### 차량 정보
        차량에 대한 기본 정보를 명확하게 나열하세요.

        ### 차량 리뷰
        리뷰 내용을 가능한 한 많이 작성하세요.  
        - 긍정적 리뷰와 부정적 리뷰를 모두 포함하세요.  
        - 차량의 성능, 디자인, 기능, 사용자 경험 등 다양한 관점에서 리뷰를 작성하세요.  
        - 사용자의 직접 경험과 구체적인 예시를 활용해 풍부한 정보를 제공하세요.

        ### 키워드 목록
        크롤링한 내용을 기반으로 차량과 관련된 키워드를 나열하세요.
        - 키워드1
        - 키워드2
        - 키워드3
        """
    )
)

# 임베딩 생성 함수
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

# 비동기 크롤링 및 요약 함수
async def crawl_and_summarize(url):
    if not url:
        return "URL이 제공되지 않았습니다. 클립보드에 URL이 복사되어 있는지 확인해주세요."
    
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=url,
            word_count_threshold=1,
            extraction_strategy=extraction_strategy,
            chunking_strategy=RegexChunking(),
            bypass_cache=True,
        )
        return result

async def summarize_and_store_url(url, save_to_db):
    """
    URL 크롤링 후 요약 반환 및 DB 저장 (옵션에 따라)
    """
    if not url:
        return "URL이 제공되지 않았습니다. 클립보드에 URL이 복사되어 있는지 확인해주세요."
    
    result = await crawl_and_summarize(url)
    if isinstance(result, str):
        return result
    if result.success:
        data = json.loads(result.extracted_content)[0]

        # 요약 결과 생성
        output = (
            f"**차량명:** {data['car_name']}\n\n"
            f"**차량이미지:** {data['car_image']}\n\n"
            f"**차량 정보:** {data['car_info']}\n\n"
            f"**차량 리뷰:** {data['car_review']}\n\n"
            f"**키워드:** {', '.join(data['keywords'])}"
        )

        # 사용자가 DB 저장을 선택한 경우 Milvus에 저장
        if save_to_db:
            text = (
                f"차량명: {data['car_name']}\n"
                f"차량이미지: {data['car_image']}\n"
                f"차량 정보: {data['car_info']}\n"
                f"차량 리뷰: {data['car_review']}\n"
                f"키워드: {', '.join(data['keywords'])}"
            )
            metadata = {
                "car_name": data["car_name"],
                "car_image": data["car_image"],
                "car_info": data["car_info"],
                "car_review": data["car_review"],
                "keywords": data["keywords"]
            }
            # KoBERT 임베딩 생성
            embedding = generate_kobert_embedding(text)

            # car_id 찾기
            car_id = find_matching_car_id(data["car_name"])
            if not car_id:
                print("car_id를 찾을 수 없습니다. 저장을 건너뜁니다.")
                return output

            # Milvus 컬렉션 준비
            collection_name = "genesis"
            if not client.has_collection(collection_name):  # 존재하지 않으면 컬렉션 생성
                create_milvus_collection(collection_name)

            # Milvus에 데이터 삽입/업데이트
            insert_or_update_data(collection_name, car_id, embedding, metadata)

            output += "\n\n**DB에 저장되었습니다.**"

        return output
    else:
        return f"페이지를 크롤링하고 요약하는 데 실패했습니다. 오류: {result.error_message}"


# Gradio를 통해 실행
def run_summarize_url(save_to_db):
    try:
        url = pyperclip.paste()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(summarize_and_store_url(url, save_to_db))
        return url, result
    except Exception as e:
        return "", f"오류가 발생했습니다: {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("# 제네시스 차량 정보 및 리뷰 요약기")
    gr.Markdown("1. 브라우저에서 요약할 제네시스 차량 페이지의 URL을 복사하세요.")
    gr.Markdown("2. 'URL 붙여넣고 요약하기' 버튼을 클릭하세요. (DB 저장 옵션 선택 가능)")
    
    save_to_db_checkbox = gr.Checkbox(label="DB에 저장하기", value=False)
    url_display = gr.Textbox(label="처리된 URL", interactive=False)
    summarize_button = gr.Button("URL 붙여넣고 요약하기")
    output = gr.Markdown(label="요약 결과")

    summarize_button.click(
        fn=lambda save_to_db: run_summarize_url(save_to_db),
        inputs=[save_to_db_checkbox],
        outputs=[url_display, output]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=9081)
