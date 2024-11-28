import sys
import os
from fastapi import FastAPI
from recommend_car.apps.routers import chatbot
sys.path.append(os.path.join(os.path.dirname(__file__), "recommend_car"))
app = FastAPI(
    title="차량 추천 전문 채팅 봇",
    description="OpenAI를 사용한 채팅 봇",
    version="1.0.0",
    debug=True
)

# 라우터 등록
app.include_router(chatbot.router, prefix="/api", tags=["Chatbot"])

@app.get("/")
async def root():
    return {"message": "Car Recommendation Chatbot API is running."}
