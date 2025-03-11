# SugarSense Diabetes Management System

## Setup and Installation

### 1️⃣ Install Dependencies
Run the following command to install all required dependencies:
```sh
pip install -r requirements.txt
```

### 2️⃣ Train the Model
Execute the following command to train the AI model:
```sh
python3 scripts/train.py
```

### 3️⃣ Test the Model
Run the following command to test the trained model:
```sh
python3 scripts/test_model.py
```

## Running the Backend API

### 4️⃣ Start the API Server
To run the FastAPI backend server, use:
```sh
uvicorn api.app:app --reload
```

## Testing the API (Optional)

### 5️⃣ Test API with cURL
You can test the AI prediction API using cURL with the following command:
```sh
curl -X 'POST' 'http://127.0.0.1:8000/ai/predict' \
-H 'Content-Type: application/json' \
-d '{
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
}'
```

## Notes
- Ensure all dependencies are installed before training or running the model.
- The API should be restarted using `uvicorn api.app:app --reload` if any changes are made to the backend.
- The AI model must be trained before making predictions.

For further details, refer to the project documentation or contact the development team.