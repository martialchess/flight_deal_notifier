import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth


load_dotenv()

SHEETY_TOKEN = os.getenv("SHEETY_BEARER_TOKEN")
SHEETY_URL = "https://api.sheety.co/90eb9c28deebc309920c1b415fe8e67b/flightDeals/prices"

HEADERS = {
    "Authorization": f"Bearer {SHEETY_TOKEN}",
    "Content-Type": "application/json"
}

class DataManager:
    def __init__(self):
        self.sheety_endpoint = SHEETY_URL
        self.destination_data = {}

    def get_data(self):
        response = requests.get(self.sheety_endpoint, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data["prices"]

    def update_data(self, row_id, new_code):
        """Update the IATA code for a specific row by ID."""
        update_endpoint = f"{self.sheety_endpoint}/{row_id}"
        body = {
            "price": {
                "iataCode": str(new_code)  # Ensure the value is sent as a string
            }
        }
        print(f"Updating row {row_id} with payload: {body}")  # Debugging
        response = requests.put(update_endpoint, json=body, headers=HEADERS)
        response.raise_for_status()
        print(f"Row {row_id} updated with IATA code {new_code}.")
        print(f"Response from Sheety: {response.json()}")  # Debugging

