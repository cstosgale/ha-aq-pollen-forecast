"""Pollen Sensor for Home Assistant"""
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from homeassistant.helpers.entity import Entity
from homeassistant import config_entries, core
from .const import DOMAIN
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import (
    CONF_LATITUDE,
    CONF_LONGITUDE
)
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType
)
from typing import Any, Callable, Dict, Optional

async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    sensors = [PollenSensor(config[CONF_LATITUDE], config[CONF_LONGITUDE])]
    async_add_entities(sensors, update_before_add=True)

async def async_setup_platform(
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """Set up the sensor platform."""
    sensors = [PollenSensor(config[CONF_LATITUDE], config[CONF_LONGITUDE])]
    async_add_entities(sensors, update_before_add=True)

class PollenSensor(Entity):
    """Representation of a Pollen Sensor."""

    def __init__(self, latitude, longitude):
        """Initialize the sensor."""
        self._state = None
        self._latitude = latitude
        self._longitude = longitude

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Pollen Sensor'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor."""
        #response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={self._latitude}&longitude={self._longitude}')
        #data = response.json()
        
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        params = {
            "latitude": self._latitude,
            "longitude": self._longitude,
            "current": "grass_pollen",
            "timezone": "Europe/London",
            "forecast_days": 1,
            "domains": "cams_europe"
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        #print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        #print(f"Elevation {response.Elevation()} m asl")
        #print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        #print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Current values. The order of variables needs to be the same as requested.
        current = response.Current()
        current_grass_pollen = current.Variables(0).Value()

        #print(f"Current time {current.Time()}")
        #print(f"Current grass_pollen {current_grass_pollen}")

        
        self._state = current_grass_pollen

