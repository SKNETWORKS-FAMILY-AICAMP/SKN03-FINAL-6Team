from fastapi import FastAPI
from apps.routers import chatbot

app = FastAPI(
    title="차량 추천 전문 채팅 봇",
    description="OpenAI를 사용한 채팅 봇",
    version="1.0.0",
)

# 라우터 등록
app.include_router(chatbot.router, prefix="/api", tags=["Chatbot"])

@app.get("/")
async def root():
    return {"message": "Car Recommendation Chatbot API is running."}
