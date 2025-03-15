from apscheduler.schedulers.background import BackgroundScheduler
import requests
import asyncio

# ✅ Check if the user logged glucose data today
async def check_and_send_reminder():
    user_id = "6057d5c3a9b6c6a1e1f5b0b4"
    response = requests.get(f"http://127.0.0.1:8000/user/health/{user_id}")
    health_data = response.json().get("health_data", [])
    
    # Check if the user has logged glucose today
    from datetime import datetime
    today =  datetime.today().strftime("%Y-%m-%d")
    has_logged_today = any(data["glucose_reading"] for data in health_data if data["day"] == today)
    
    if not has_logged_today:
        requests.post(
            "http://127.0.0.1:8000/user/send_notification",
            json={
                "user_id": user_id,
                "title": "Reminder: Log Your Glucose",
                "body": "📋 You forgot to log today’s glucose reading. Please update your health data!"
            }
        )
        print("📢 Reminder sent to user.")
        
# ✅ Run Scheduler Every 24 Hours
scheduler = BackgroundScheduler()
scheduler.add_job(lambda: asyncio.run(check_and_send_reminder()), "interval", hours=24)
scheduler.start()