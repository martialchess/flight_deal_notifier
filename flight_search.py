import requests
import os
import time
from dotenv import load_dotenv
from flight_data import FlightData


load_dotenv()


class FlightSearch:
    """
    Handles fetching IATA codes from Amadeus API with token caching.
    """

    TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
    LOCATION_URL = "https://test.api.amadeus.com/v1/reference-data/locations"

    def __init__(self):
        self._api_key = os.getenv("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_API_SECRET")
        if not self._api_key or not self._api_secret:
            raise ValueError("AMADEUS_API_KEY or AMADEUS_API_SECRET not found in environment variables")
        self._token = None
        self._token_expiry = 0  # timestamp when token expires

    def _get_token(self):
        """
        Returns a valid access token, fetching a new one if expired.
        """
        if self._token and time.time() < self._token_expiry:
            # Token still valid
            return self._token

        # Request new token
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }

        response = requests.post(url=self.TOKEN_URL, headers=headers, data=data)
        if response.status_code != 200:
            raise Exception(f"Failed to get token: {response.status_code} - {response.text}")

        token_data = response.json()
        self._token = token_data["access_token"]
        self._token_expiry = time.time() + int(token_data["expires_in"]) - 10  # small buffer
        print(f"[DEBUG] New access token fetched, expires in {token_data['expires_in']} seconds")
        return self._token

    def get_destination_code(self, city_name):
        """
        Fetches IATA code for a given city name.
        """
        token = self._get_token()
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "subType": "CITY",
            "keyword": city_name,
            "page[limit]": 1
        }

        response = requests.get(url=self.LOCATION_URL, headers=headers, params=params)

        if response.status_code != 200:
            print(f"[ERROR] Failed to fetch IATA code for {city_name}: {response.status_code}")
            return None

        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            iata_code = data["data"][0]["iataCode"]
            print(f"[DEBUG] IATA code for {city_name} is {iata_code}")
            return iata_code
        else:
            print(f"[WARNING] No IATA code found for {city_name}")
            return None

    def search_flights(self, origin_city, destination_city, from_date, to_date, currency="GBP", non_stop=True):
        """
        Searches for flights using the Amadeus API and returns a FlightData object.
        """
        token = self._get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        body = {
            "currencyCode": currency,
            "originDestinations": [
                {
                    "id": "1",
                    "originLocationCode": origin_city,
                    "destinationLocationCode": destination_city,
                    "departureDateTimeRange": {
                        "date": from_date
                    },
                    "returnDateTimeRange": {
                        "date": to_date
                    }
                }
            ],
            "travelers": [
                {
                    "id": "1",
                    "travelerType": "ADULT"
                }
            ],
            "sources": ["GDS"],
            "searchCriteria": {
                "flightFilters": {
                    "nonStop": non_stop
                }
            }
        }
        response = requests.post(
            url="https://test.api.amadeus.com/v2/shopping/flight-offers",
            headers=headers,
            json=body
        )
        if response.status_code != 200:
            print(f"[ERROR] Failed to fetch flight data: {response.status_code} - {response.text}")
            return None

        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            offer = data["data"][0]
            price = offer["price"]["total"]
            itinerary = offer["itineraries"][0]
            out_segment = itinerary["segments"][0]
            origin_airport = out_segment["departure"]["iataCode"]
            destination_airport = out_segment["arrival"]["iataCode"]
            out_date = out_segment["departure"]["at"].split("T")[0]
            return_segment = itinerary["segments"][-1]
            return_date = return_segment["arrival"]["at"].split("T")[0]
            # For city names, you may need to map IATA codes to city names if needed
            flight_data = FlightData(
                price=price,
                origin_city=origin_city,
                origin_airport=origin_airport,
                destination_city=destination_city,
                destination_airport=destination_airport,
                out_date=out_date,
                return_date=return_date
            )
            return flight_data
        else:
            print("[WARNING] No flight data found.")
            return None


# Example usage
if __name__ == "__main__":
    fs = FlightSearch()
    print(fs.get_destination_code("London"))
    print(fs.get_destination_code("Paris"))  # will reuse token if not expired
