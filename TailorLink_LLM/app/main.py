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

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용 (개발 시에만 사용)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
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
    uvicorn.run("app.main:app", host="0.0.0.0", port=7000, reload=True)