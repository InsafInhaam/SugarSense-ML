from fastapi import APIRouter, HTTPException, Depends
from api.database import health_collection
from api.models import HealthData

router = APIRouter()

# ✅ Store Health Data
@router.post("/health")
async def store_health_data(data: HealthData):
    new_entry = await health_collection.insert_one(data.dict())
    return {"message": "Health data stored successfully", "entry_id": str(new_entry.inserted_id)}

# ✅ Get User Health Data
@router.get("/health/{user_id}")
async def get_health_data(user_id: str):
    data = await health_collection.find({"user_id": user_id}).to_list(100)
    return {"user_id": user_id, "health_data": data}
