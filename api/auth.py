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
    
    new_user = await users_collection.insert_one(user_data)
    return {"message": "User registered successfully", "user_id": str(new_user.inserted_id)}

# ✅ Login User
@router.post("/login")
async def login_user(request: LoginRequest):
    user = await users_collection.find_one({"email": request.email})
    if not user or not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_jwt_token({"email": user['email']})
    return {"message": "Health data stored successfully", "entry_id": str(new_entry.inserted_id)}

# ✅ Get User Health Data
@router.get("/health/{user_id}")
async def get_health_data(user_id: str):
    data = await health_collection.find({"user_id": user_id}).to_list(100)
    return {"user_id": user_id, "health_data": data}

