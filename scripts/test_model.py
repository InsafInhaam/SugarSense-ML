import joblib  # ✅ Fix: Ensure joblib is imported
import pandas as pd
import numpy as np

# Load saved model & scaler
model = joblib.load("models/glucose_prediction_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# Example user input
new_data = pd.DataFrame([{
    "meal_intake": 50,
    "insulin_dose": 10,
    "exercise_minutes": 30,
    "medication_taken": 1,
    "sleep_hours": 7,
    "stress_level": 3,
    "year": 2025,
    "month": 3,
    "day": 9,
    "hour": 14
}])

# Scale input data
new_data_scaled = scaler.transform(new_data)

# Predict glucose level
predicted_glucose = model.predict(new_data_scaled)
print(f"🩸 Predicted Glucose Level: {predicted_glucose[0]:.2f} mg/dL")
