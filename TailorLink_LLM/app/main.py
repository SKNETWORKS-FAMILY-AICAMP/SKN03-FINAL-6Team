from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.features.recommend_car.apps.routers import chatbot as recommend_bot
from app.features.manual.router import chatbot as manual_bot
from app.core.lifespan import lifespan
from app.core.config import settings
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,  # lifespan 컨텍스트 추가
)

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 Origin (특정 도메인을 설정하는 것이 보안에 더 좋음)
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메서드
    allow_headers=["*"],  # 허용할 HTTP 헤더
)

# 라우터 등록
app.include_router(recommend_bot.car_recommend_router, prefix="/api/cars", tags=["car_recommend_Chatbot"])
app.include_router(manual_bot.manual_qa_router, prefix="/api/manuals", tags=["manual_qa"])

@app.get("/")
async def root():
    return {"message": "Car Chatbot API is running."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)