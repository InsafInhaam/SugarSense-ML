from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://insafinhaam732:Aq3fSwDMjAQOTnhG@cluster0.zu4xm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "sugarsense"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db["users"]
health_collection = db["health_data"]