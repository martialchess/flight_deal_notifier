# Flight Deals Notifier

## Overview
This project automates the search for cheap round-trip flights from London to various international destinations. It updates a Google Sheet with IATA codes, queries the Amadeus API for flight prices, and sends WhatsApp alerts via Twilio when a flight price drops below your target.

## Technologies Used
- **Python 3**
- **Amadeus API** (for flight search and IATA codes)
- **Sheety API** (for Google Sheets integration)
- **Twilio API** (for WhatsApp notifications)
- **dotenv** (for environment variable management)

## What We Learned
- How to interact with multiple APIs (Amadeus, Sheety, Twilio) in Python.
- Structuring code with classes for maintainability (`FlightSearch`, `FlightData`, `DataManager`, `NotificationManager`).
- Handling API authentication and token management.
- Parsing and validating API responses.
- Sending WhatsApp messages programmatically.
- Debugging common mistakes (e.g., incorrect parameter formats, missing required fields, handling booleans in JSON, Twilio sandbox setup).

## Challenges & Solutions
- **Incorrect API Parameter Formats:**  
  We learned that Amadeus expects nested JSON arrays and booleans, not flat dictionaries or strings. Fixing this required careful reading of the API docs and restructuring requests.
- **IATA Code Validation:**  
  Some sheet rows had invalid or missing IATA codes, causing errors. We added type checks and fallback logic.
- **Twilio WhatsApp Sandbox:**  
  Messages weren't delivered until we joined the Twilio sandbox and used the correct number format.
- **Error Handling:**  
  We added robust error handling for API failures, rate limits, and missing data.

## Real World Use Cases
- **Travel Agencies:** Automate fare monitoring and alert customers to deals.
- **Personal Use:** Get notified when your dream destination is affordable.
- **Market Research:** Track price trends for flights.

## Future Improvements
- Add support for more origin cities.
- Integrate with email or SMS (not just WhatsApp).
- Store historical price data for analytics.
- Add a web dashboard for easier management.
- Use production Twilio numbers for broader notifications.

## How to Run
1. Clone the repo: https://github.com/martialchess/flight_deal_notifier.git
2. Create a `.env` file with your API keys (see `.env.example`).
3. Activate your Python virtual environment.
4. Install dependencies:  
   `pip install -r requirements.txt`
5. Run `main.py`.

## License
MIT
