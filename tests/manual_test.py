"""Test function to test API request"""

import sys
import os
import requests
import json

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath('../'))

from custom_components.aq_pollen_forecast.sensor import get_max_value_for_date
from custom_components.aq_pollen_forecast.const import (
    AQAPI_CURRENT,
    AQAPI_HOURLY,
    AQAPI_URL
)

def make_api_request(url, params):
    """Makes an API Request"""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Assuming the response is in JSON format
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

params={
                    "latitude": "52.52",
                    "longitude": "13.41",
                    "current": AQAPI_CURRENT,
                    "hourly": AQAPI_HOURLY,
                    "timezone": "Europe/London",
                    "forecast_days": 4
                }


data = make_api_request(AQAPI_URL, params)

formatted_json = json.dumps(data, indent=4)

print(AQAPI_HOURLY)

# Print the formatted JSON string
print(formatted_json)

max_value = get_max_value_for_date(data, "ozone", "1d")

print("Max value is", max_value)
