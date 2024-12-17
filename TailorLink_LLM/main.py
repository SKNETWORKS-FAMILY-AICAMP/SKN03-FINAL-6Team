import sys
import os
import logging
from logging.handlers import RotatingFileHandler
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommend_car.apps.routers import chatbot
# from recommend_car.apps.data_update_crawling import update_car_models
from doc_retrieval_qa.router import qabot


logging.basicConfig(
    level=logging.DEBUG,  
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # 로그 출력 포맷
    handlers=[
        logging.StreamHandler(),  # 터미널 출력
        RotatingFileHandler("app.log", maxBytes=10 * 1024 * 1024, backupCount=5),  # 로그 파일 크기 제한
    ],
)
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.setLevel(logging.DEBUG)

# 로깅 추가
logger = logging.getLogger("TailorLink Chatbot")
logger.info("TailorLink FastAPI 애플리케이션 시작!")

app = FastAPI(
    title="차량 전문 채팅 봇",
    description="OpenAI를 사용한 채팅 봇",
    version="1.0.1",
    debug=True
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용 (개발 시에만 사용)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 라우터 등록
app.include_router(chatbot.car_recommend_router, prefix="/api/cars", tags=["car_recommend_Chatbot"])
app.include_router(qabot.manual_qa_router, prefix="/api/manuals", tags=["manual_qa"])

@app.get("/")
async def root():
    return {"message": "Car Chatbot API is running."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# # 주기적 작업 실행 함수
# async def periodic_update():
#     while True:
#         logger.info("자동 업데이트 진행 중")
#         # 비동기적으로 블로킹 함수 실행
#         await asyncio.to_thread(update_car_models)
#         await asyncio.sleep(60 * 60 * 24 * 7)  # 일주일(7일) 대기

# # 애플리케이션 시작 시 주기적 업데이트 작업 시작
# @app.on_event("startup")
# async def startup_event():
#     logger.info("업데이트 시작")
#     asyncio.create_task(periodic_update())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)