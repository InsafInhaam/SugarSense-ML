from pydantic import BaseModel, EmailStr
from typing import Optional, List

# ✅ User Schema
class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    fcm_token: Optional[str] = None
    
# ✅ Login Schema
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    fcm_token: Optional[str] = None
    
# ✅ Health Data Schema
class HealthData(BaseModel):
    user_id: str
    glucose_reading: Optional[float] = None
    meal_intake: Optional[str] = None
    meal_portion: Optional[float] = None
    exercise_minutes: Optional[int] = None
    insulin_dose: Optional[float] = None
    medication_taken: Optional[bool] = None
    medical_reports: Optional[List[str]] = []
    
# ✅ Define a Pydantic model for request body validation
class NotificationRequest(BaseModel):
    user_id: str
    title: str
    body: str
    
class FCMTokenRequest(BaseModel):
    user_id: str
    fcm_token: str
    
class FCMTokenUpdate(BaseModel):
    user_id: str
    fcm_token: str