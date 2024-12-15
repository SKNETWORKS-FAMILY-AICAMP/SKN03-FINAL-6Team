import os
import json
import asyncio
import gradio as gr
import pyperclip
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai.chunking_strategy import RegexChunking
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# 제네시스 차량 정보를 저장할 데이터 모델 정의
class GenesisCarInfo(BaseModel):
    car_name: str = Field(..., description="차량명")
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
        크롤링한 내용에서 다음 세부 정보를 추출하고 반드시 한국어로 번역해서 출력하세요:
        1. 차량명 
        2. 차량 정보
        3. 차량 리뷰
        4. 페이지에 할당된 키워드 목록.

        결과는 다음과 같은 JSON 형식이어야 합니다:
        { "car_name": "차량명", "car_info": "차량 정보", "car_review": "차량 리뷰", "keywords": ["키워드1", "키워드2", "키워드3"] }
        """
    )
)

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

async def summarize_url(url):
    if not url:
        return "URL이 제공되지 않았습니다. 클립보드에 URL이 복사되어 있는지 확인해주세요."
    
    result = await crawl_and_summarize(url)
    if isinstance(result, str):
        return result
    if result.success:
        data = json.loads(result.extracted_content)[0]
        
        output = (
            f"**차량명:** {data['car_name']}\n\n"
            f"**차량 정보:** {data['car_info']}\n\n"
            f"**차량 리뷰:** {data['car_review']}\n\n"
            f"**키워드:** {', '.join(data['keywords'])}"
        )
        return output
    else:
        return f"페이지를 크롤링하고 요약하는 데 실패했습니다. 오류: {result.error_message}"

def run_summarize_url():
    try:
        url = pyperclip.paste()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(summarize_url(url))
        return url, result
    except Exception as e:
        return "", f"오류가 발생했습니다: {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("# 제네시스 차량 정보 및 리뷰 요약기")
    gr.Markdown("1. 브라우저에서 요약할 제네시스 차량 페이지의 URL을 복사하세요.")
    gr.Markdown("2. 'URL 붙여넣고 요약하기' 버튼을 클릭하세요.")
    
    url_display = gr.Textbox(label="처리된 URL", interactive=False)
    summarize_button = gr.Button("URL 붙여넣고 요약하기")
    output = gr.Markdown(label="요약 결과")

    summarize_button.click(
        fn=run_summarize_url,
        outputs=[url_display, output]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=9081)