import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load synthetic dataset
df = pd.read_csv("synthetic_glucose_data.csv")

# Display sample data
print("Dataset Sample:")
print(df.head())

# Ensure column names are formatted correctly
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Convert timestamp to datetime and extract useful features
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["year"] = df["timestamp"].dt.year
df["month"] = df["timestamp"].dt.month
df["day"] = df["timestamp"].dt.day
df["hour"] = df["timestamp"].dt.hour

# Drop original timestamp column (since it's not usable in ML directly)
df.drop(columns=["timestamp"], inplace=True)

# Features & Target
X = df.drop(columns=["glucose_level"])  # Input Features
y = df["glucose_level"]  # Target Variable

# Train-Test Split (80-20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature Scaling (Standardization)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train XGBoost Regressor
model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1, max_depth=5)
model.fit(X_train_scaled, y_train)

# Model Predictions
y_pred = model.predict(X_test_scaled)

# Model Evaluation
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n📊 Model Performance:")
print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")
print(f"R² Score: {r2:.2f}")

# Save Model & Scaler
joblib.dump(model, "glucose_prediction_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\n✅ Model training complete. Saved as 'glucose_prediction_model.pkl'")
