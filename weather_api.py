
import sys
import argparse

from wx_utils import (
    get_user_location,
    get_coordinates,
    generate_location_url,
    safe_api_call,
    get_forecast_url,
    parse_forecast_response,
    print_forecast
)
from wx_config import forecast_locations


def parse_args():
    parser = argparse.ArgumentParser(
        description='Get weather forecast for a location'
    )
    parser.add_argument('location',
                        nargs='?',  # Makes it optional
                        help='Location name (e.g., "death valley")')
    return parser.parse_args()


def main():
    args = parse_args()
    print("Welcome to weather app!")

    # Use CLI arg is provided, otherwise prompt user
    if args.location:
        location = args.location.lower().strip()
        # Validate it exists in forecast_locations
        if location not in forecast_locations:
            print(f"Invalid location: {location}")
            print(f"Choose from: {', '.join(forecast_locations.keys())}")
            location = get_user_location()
    else:
        # Fall back to interactive prompt
        print(
            "Select a location from this list\n",
            f"{', '.join(forecast_locations).title()}"
        )
        location = get_user_location()

    coords = get_coordinates(location)

    loc_url = generate_location_url(coords.latitude, coords.longitude)

    if not loc_url:
        print("URL for this location not returned")
        sys.exit(1)
    else:
        location_resp = safe_api_call(loc_url)

    if not location_resp:
        print('No location data :(')
        sys.exit(1)
    else:
        forecast_url = get_forecast_url(location_resp)

    if not forecast_url:
        print("Forecast URL not returned")
        sys.exit(1)

    forecast_resp = safe_api_call(forecast_url)

    if not forecast_resp:
        print(f"No forecast data for this location: {location}")
        sys.exit(1)
    else:
        forecast_data = parse_forecast_response(forecast_resp, location)
        if forecast_data:
            print_forecast(forecast_data)


if __name__ == '__main__':
    main()
