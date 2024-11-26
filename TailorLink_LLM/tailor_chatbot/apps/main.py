from fastapi import FastAPI
from apps.routers import chatbot

app = FastAPI(
    title="Car Recommendation Chatbot API",
    description="A chatbot API for recommending cars using OpenAI.",
    version="1.0.0",
)

# 라우터 등록
app.include_router(chatbot.router, prefix="/api", tags=["Chatbot"])

@app.get("/")
async def root():
    return {"message": "당신이 구매하고자 하는 차량, 추천해드리겠습니다."}

