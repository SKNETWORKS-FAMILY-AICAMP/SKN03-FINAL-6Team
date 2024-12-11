import sys
import os
import logging
import asyncio
from fastapi import FastAPI
from recommend_car.apps.routers import chatbot
from recommend_car.apps.data_update_crawling import update_car_models

logging.basicConfig(
    level=logging.DEBUG,  
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # 로그 출력 포맷
    handlers=[
        logging.StreamHandler(),  # 터미널 출력
        logging.FileHandler("app.log"),  # 파일 출력
    ],
)

logger = logging.getLogger("recommend_car")

uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.setLevel(logging.DEBUG)

app = FastAPI(
    title="차량 추천 전문 채팅 봇",
    description="OpenAI를 사용한 채팅 봇",
    version="1.0.0",
    debug=True
)

# 로깅 추가
logger = logging.getLogger("recommend_car")
logger.info("FastAPI 애플리케이션 시작!")

# 라우터 등록
app.include_router(chatbot.car_recommend_router, prefix="/api", tags=["car_recommend_Chatbot"])

@app.get("/")
async def root():
    return {"message": "Car Recommendation Chatbot API is running."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# 주기적 작업 실행 함수
async def periodic_update():
    while True:
        logger.info("자동 업데이트 진행 중")
        # 비동기적으로 블로킹 함수 실행
        await asyncio.to_thread(update_car_models)
        await asyncio.sleep(60 * 60 * 24 * 7)  # 일주일(7일) 대기

# 애플리케이션 시작 시 주기적 업데이트 작업 시작
@app.on_event("startup")
async def startup_event():
    logger.info("업데이트 시작")
    asyncio.create_task(periodic_update())


