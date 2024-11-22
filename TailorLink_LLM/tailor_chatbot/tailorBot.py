from fastapi import FastAPI
from routers import recommend

app = FastAPI(
    title="차량 추천 엔진",
    description="사용자의 선호도에 맞는 차량을 추천합니다.",
    version="1.0.0"
)

app.include_router(recommend.router)