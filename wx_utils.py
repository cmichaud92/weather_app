import requests
import sys
from wx_config import (
    forecast_locations,
    Coordinates,
    BASE_URL
)


def get_user_location() -> str:
    while True:
        location: str = (
            input("Enter a location (or 'quit' to exit): ")
            .lower()
            .strip()
        )
        if location == 'quit':
            print("Exiting Weather App...")
            sys.exit(1)
        if location in forecast_locations:
            return location
        print(
            f"{location} is not a valid location."
            f"Please choose from {', '.join(forecast_locations)}")


def get_coordinates(location: str) -> Coordinates:
    location = location.lower().strip()
    if location not in forecast_locations:
        raise ValueError(f"Unknown location: {location}")
    coords = forecast_locations[location]['coordinates']
    return Coordinates(coords['latitude'], coords['longitude'])


def generate_location_url(lat: float, lon: float, base_url: str = BASE_URL):
    return f"{base_url}/points/{lat},{lon}"


def make_api_call(url: str) -> dict | None:
    resp = requests.get(url)
    resp.raise_for_status()  # Returns an error if api call encountered issues
    return resp.json()       # Converts result text into a dict type


def safe_api_call(url: str) -> dict | None:
    try:
        return make_api_call(url)
    except requests.exceptions.ConnectionError as e:
        print(f"connection error: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected exception occurred: {e}")
        return None


def get_forecast_url(location_resp: dict) -> str | None:
    try:
        return location_resp['properties']['forecast']
    except (KeyError, TypeError):
        print("Unexpected API response structure")
        return None


def parse_forecast_response(forecast_resp: dict, location: str) -> dict | None:
    try:
        return {location: forecast_resp['properties']['periods']}
    except (KeyError, TypeError):
        print("Unexpected API response structure")
        return None


def print_forecast(forecast_data: dict) -> None:
    for loc, data in forecast_data.items():
        print(f"NWS Forecast for {loc.title()}")
        for record in data:
            print(f"  - {record['name']}: {record['detailedForecast']}")
