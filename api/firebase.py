import firebase_admin
from firebase_admin import credentials, messaging
import os 

# Initialize Firebase
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(BASE_DIR, "serviceAccountKey.json")

cred = credentials.Certificate(cred_path) 
firebase_admin.initialize_app(cred)

# Function to send push notifications
def send_notification(token, title, body):
    message = messaging.Message(
        notification = messaging.Notification(
            title=title,
            body=body
        ),
        token=token
    )
    response = messaging.send(message)
    return response