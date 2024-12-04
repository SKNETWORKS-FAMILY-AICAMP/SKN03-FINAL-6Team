import sys
import os
import logging
from fastapi import FastAPI
from recommend_car.apps.routers import chatbot
sys.path.append(os.path.join(os.path.dirname(__file__), "recommend_car"))

logging.basicConfig(
    level=logging.DEBUG,  # DEBUG 레벨로 설정하여 모든 로그가 출력되도록
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
app.include_router(chatbot.router, prefix="/api", tags=["Chatbot"])

@app.get("/")
async def root():
    return {"message": "Car Recommendation Chatbot API is running."}

