from fastapi import APIRouter, HTTPException
from models.preferences import Preferences
from services.recommendation_service import get_recommendations

router = APIRouter()

@router.post("/recommendations")
async def recommend_vehicle(preferences: Preferences):
    try:
        recommendations = get_recommendations(preferences.preferences)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
