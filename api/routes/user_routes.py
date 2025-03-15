from fastapi import APIRouter, HTTPException
from api.database import users_collection
from pydantic import BaseModel
from api.models import FCMTokenUpdate

router = APIRouter()

@router.post("/update_fcm_token")
async def update_fcm_token(data: FCMTokenUpdate):
    result = await users_collection.update_one(
        {"_id": data.user_id},
        {"$set": {"fcm_token": data.fcm_token}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "FCM token updated successfully"}
