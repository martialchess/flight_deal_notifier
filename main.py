# This file will need to use the DataManager, FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
import time  # Import time module for sleep functionality
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# --- ENV VARS ---
load_dotenv()
app_id = os.getenv("APP_ID")
sheety_api_key = os.getenv("SHEETY_API_KEY")

# Fetch sheet data
sheet_data = data_manager.get_data()
print("Original sheet data:")
pprint(sheet_data)

# Loop through rows and update if missing iataCode
for row in sheet_data:
    # Check if 'iataCode' exists and is empty
    if row.get("iataCode") in [None, ""]:
        if "city" in row and row["city"]:  # Ensure 'city' exists and is not empty
            try:
                # Fetch IATA code using FlightSearch
                new_code = flight_search.get_destination_code(row["city"])
                if new_code:  # Only update if a valid IATA code is returned
                    row["iataCode"] = new_code
                    # Push update back to Sheety
                    data_manager.update_data(row["id"], new_code)
                else:
                    print(f"[WARNING] No IATA code found for city: {row['city']}")
            except Exception as e:
                print(f"[ERROR] Failed to fetch IATA code for city: {row['city']}. Error: {e}")
            finally:
                # Add a delay to avoid hitting the API rate limit
                time.sleep(1)

print("\nUpdated sheet data:")
pprint(sheet_data)

# --- Search for Flight Prices ---
origin_city = "LON"  # London
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
six_months_later = (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d")

print("\nSearching for flight prices...")
for row in sheet_data:
    destination_code = row.get("iataCode")
    city = row.get("city")
    lowest_price = row.get("lowestPrice")
    # Ensure destination_code is a string and 3 letters
    if isinstance(destination_code, str) and len(destination_code) == 3:
        try:
            flight = flight_search.search_flights(
                origin_city=origin_city,
                destination_city=destination_code,
                from_date=tomorrow,
                to_date=six_months_later,
                currency="GBP",
                non_stop=True
            )
            if flight:
                print(flight)
                # Check if flight price is lower than sheet price
                if lowest_price and float(flight.price) < float(lowest_price):
                    sms_message = (
                        f"Low price alert! Only £{flight.price} to fly from "
                        f"{flight.origin_airport} to {flight.destination_airport}.\n"
                        f"Outbound: {flight.out_date}\nInbound: {flight.return_date}"
                    )
                    notification_manager.send_sms(sms_message)
            else:
                print(f"{city}: N/A")
        except Exception as e:
            print(f"[ERROR] Failed to fetch flight data for {city}. Error: {e}")
        finally:
            time.sleep(1)
    else:
        print(f"{city}: N/A (Invalid IATA code: {destination_code})")
