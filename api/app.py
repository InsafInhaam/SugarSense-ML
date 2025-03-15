from fastapi import FastAPI
from api.auth import router as auth_router
from api.routes.health_routes import router as health_router
from api.predict import router as predict_router
from api.scheduler import scheduler

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(health_router, prefix="/user", tags=["User Health Data"])
app.include_router(predict_router, prefix="/ai", tags=["AI Predictions"])

# Root Endpoint
@app.get("/")
def home():
    return {"message": "SugarSense API Running 🚀"}