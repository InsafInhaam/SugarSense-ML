from fastapi import APIRouter
import joblib
import pandas as pd
import numpy as np
from pydantic import BaseModel
import os

# Get absolute path for model files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../models/glucose_prediction_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "../models/scaler.pkl")

# Load trained model & scaler
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# Create FastAPI Router
router = APIRouter()

# Request Body Schema
class GlucoseInput(BaseModel):
    meal_intake: float
    insulin_dose: float
    exercise_minutes: float
    medication_taken: int
    sleep_hours: float
    stress_level: float
    year: int
    month: int
    day: int
    hour: int

# ✅ Prediction API Endpoint
@router.post("/predict")
def predict_glucose(data: GlucoseInput):
    # Convert input to DataFrame
    input_data = pd.DataFrame([data.dict()])
    
    # Scale input using saved scaler
    input_scaled = scaler.transform(input_data)

    # Predict glucose level
    predicted_glucose = model.predict(input_scaled)[0]

    return {"predicted_glucose_level": float(predicted_glucose)}