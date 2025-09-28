from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        self.from_number = os.getenv("TWILIO_FROM")
        self.to_number = os.getenv("TWILIO_TO")

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=self.to_number
        )
        print(f"[INFO] SMS sent: SID {message.sid}")