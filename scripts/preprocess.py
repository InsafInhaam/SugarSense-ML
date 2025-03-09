import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib

# 1️⃣ Load the dataset
df = pd.read_csv("synthetic_glucose_data.csv")

# 2️⃣ Convert timestamp to datetime and extract features
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["year"] = df["timestamp"].dt.year
df["month"] = df["timestamp"].dt.month
df["day"] = df["timestamp"].dt.day
df["hour"] = df["timestamp"].dt.hour

# Drop original timestamp column
df.drop(columns=["timestamp"], inplace=True)

# 3️⃣ Handle missing values (if any)
df.fillna(df.median(), inplace=True)  # Replace missing values with median

# 4️⃣ Define Features & Target
X = df.drop(columns=["glucose_level"])  # Input Features
y = df["glucose_level"]  # Target Variable (What we are predicting)

# 5️⃣ Train-Test Split (80% training, 20% testing)
X_train, _test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6️⃣ Feature Scaling (Normalization)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save the scaler for later use
joblib.dump(scaler, "scaler.pkl")

print("✅ Data preprocessing complete.")
