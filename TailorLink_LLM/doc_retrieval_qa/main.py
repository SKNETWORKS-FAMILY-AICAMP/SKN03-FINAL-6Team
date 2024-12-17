from typing import Union
from urllib.request import Request

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import asyncio

from core.milvus_connector import connect_to_milvus

from RAG.rag_pipeline import run_rag
app = FastAPI()
connect_to_milvus()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용 (개발 시에만 사용)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

class RequestQuestion(BaseModel):
    question: str
    session_id: str


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/manual")
async def ask_query(request: RequestQuestion):
    question = request.question

    async def mock_stream_openai_response(prompt):
        accumulated_text = ""  # 누적 텍스트 저장
        res = run_rag(prompt)
        print(type(res))
        for letter in res:
            accumulated_text += letter  # 텍스트 누적
            yield json.dumps({"status": "processing", "data": letter}, ensure_ascii=False) + "\n"
            await asyncio.sleep(0.05)  # 스트림 딜레이 시뮬레이션

        yield json.dumps({"status": "complete", "data": "Stream finished"}, ensure_ascii=False) + "\n"

    return StreamingResponse(mock_stream_openai_response(question), media_type="text/event-stream")

@app.post("/ask_query")
async def ask_query(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")
    print(prompt)
    async def mock_stream_openai_response(prompt):
        accumulated_text = ""  # 누적 텍스트 저장
        for letter in prompt:
            accumulated_text += letter  # 텍스트 누적
            yield json.dumps({"status": "processing", "data": letter}, ensure_ascii=False) + "\n"
            await asyncio.sleep(0.1)  # 스트림 딜레이 시뮬레이션

        yield json.dumps({"status": "complete", "data": "Stream finished"}, ensure_ascii=False) + "\n"

    return StreamingResponse(mock_stream_openai_response(prompt), media_type="text/event-stream")
