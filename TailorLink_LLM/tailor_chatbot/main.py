# main.py
import uvicorn
from fastapi import FastAPI

# app 디렉토리에서 생성한 객체들을 임포트
from app.routers import chat

app = FastAPI()

# 라우터 등록
app.include_router(chat.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
