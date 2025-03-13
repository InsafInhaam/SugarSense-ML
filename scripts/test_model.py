import joblib
import pandas as pd
import numpy as np
import requests
import datetime
import json

# Load saved model & scaler
model = joblib.load("models/glucose_prediction_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# Example user input
new_data = pd.DataFrame([{
    "meal_intake": 70,       # Carbs in grams
    "insulin_dose": 8,       # Insulin dose in units
    "exercise_minutes": 20,  # Exercise in minutes
    "medication_taken": 1,   # 1 = Yes, 0 = No
    "sleep_hours": 6.5,      # Sleep in hours
    "stress_level": 4,       # Stress level (1-5)
    "year": datetime.datetime.now().year,
    "month": datetime.datetime.now().month,
    "day": datetime.datetime.now().day,
    "hour": datetime.datetime.now().hour
}])

# Scale input data
new_data_scaled = scaler.transform(new_data)

# Predict glucose level
predicted_glucose = model.predict(new_data_scaled)
# print(f"🩸 Predicted Glucose Level: {predicted_glucose[0]:.2f} mg/dL")

# define a sample user id
user_id = "6057d5c3a9b6c6a1e1f5b0b4"

notifications = []

# AI-driven notification logic
if predicted_glucose < 70:
    notifications.append("⚠️ **Hypoglycemia Risk:** Your glucose may drop in 2 hours. Have a small snack.")

if predicted_glucose > 180:
    notifications.append("🚨 **High Glucose Alert!** Your levels are elevated. Check your insulin dosage.")

if new_data["meal_intake"][0] > 60:
    notifications.append("🍛 **Carb Alert!** High-carb meals cause glucose spikes. Consider adding fiber.")

if new_data["exercise_minutes"][0] < 15:
    notifications.append("🏃 **Increase Activity:** Light exercise can help regulate glucose levels.")

if new_data["sleep_hours"][0] < 6:
    notifications.append("💤 **Lack of Sleep Detected:** Poor sleep can lead to insulin resistance.")

if new_data["stress_level"][0] >= 4:
    notifications.append("🧘 **High Stress Level:** Stress impacts glucose. Try relaxation techniques.")
    
# Send Notification if Needed
for message in notifications:
    response = requests.post(
        "http://127.0.0.1:8000/user/send_notification",
        json={"user_id": user_id, "title": "Glucose Alert", "body": message}
    )
    print(f"📢 Notification Sent: {message}")
        
# Log prediction & notification
log_entry = {
    "user_id": user_id,
    "timestamp": datetime.datetime.now().isoformat(),
    "input_date": new_data.to_dict(orient="records")[0],
    "predicted_glucose": round(float(predicted_glucose[0]), 2),
    "notifications": notifications
}

# Save logs to a json file
with open("logs/glucose_predictions.json", "a") as log_file:
    log_file.write(json.dumps(log_entry) + "\n")
    
print(f"✅ Prediction logged successfully: {log_entry}")