from fastapi import APIRouter, HTTPException, Depends
from api.database import users_collection
from api.models import User, LoginRequest
from passlib.context import CryptContext
import jwt

router = APIRouter()

SECRET_KEY = "dnucn73b7d@cs"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# ✅ Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) 

# ✅ Generate JWT Token
def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

# ✅ Register User
@router.post("/register")
async def register_user(user: User):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password
    
    if "fcm_token" not in user_data:
        user_data["fcm_token"] = None

    new_user = await users_collection.insert_one(user_data)
    return {"message": "User registered successfully", "user_id": str(new_user.inserted_id)}

# ✅ Login User
@router.post("/login")
async def login_user(request: LoginRequest):
    user = await users_collection.find_one({"email": request.email})
    if not user or not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token({"email": user["email"]})
    
    # Automatically update FCM Token when user logs in
    if request.fcm_token:
        await users_collection.update_one(
            {"email": request.email},
            {"$set": {"fcm_token": request.fcm_token}}
        )
    
    return {"message": "Login successful", "token": token}
