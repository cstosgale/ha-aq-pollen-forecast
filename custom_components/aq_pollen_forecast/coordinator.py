"""Open Meteo Coordinator."""
# For API Documentation see https://open-meteo.com/en/docs/air-quality-api

from datetime import timedelta
import logging
from homeassistant.const import ( # type: ignore
    CONF_LATITUDE,
    CONF_LONGITUDE
)
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError # type: ignore
from homeassistant.helpers.update_coordinator import ( # type: ignore
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    AQAPI_URL,
    AQAPI_CURRENT,
    AQAPI_HOURLY
)

_LOGGER = logging.getLogger(__name__)

class OPENMETEOCoordinator(DataUpdateCoordinator):
    """Data coordinator."""

    def __init__(self, hass, session, data):
        """Initialize coordinator."""

        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="OPENMETEO",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=3600),
        )
        self.session = session
        self._latitude = data[CONF_LATITUDE]
        self._longitude = data[CONF_LONGITUDE]

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            resp = await self.session.request(
                method="GET",
                url=AQAPI_URL,
                params={
                    "latitude": self._latitude,
                    "longitude": self._longitude,
                    "current": AQAPI_CURRENT,
                    "hourly": AQAPI_HOURLY,
                    "timezone": "Europe/London",
                    "forecast_days": 4
                }
            )
            body = await resp.json()
        except InvalidAuth as err:
            raise ConfigEntryAuthFailed from err
        except OPENMETEOError as err:
            raise UpdateFailed(str(err)) from err
        except ValueError as err:
            err_str = str(err)

            if "Invalid authentication credentials" in err_str:
                raise InvalidAuth from err
            if "API rate limit exceeded." in err_str:
                raise APIRatelimitExceeded from err

            _LOGGER.exception("Unexpected exception")
            raise UnknownError from err

        if "error" in body:
            error = body["reason"]
            raise UnknownError(
                f"AQAPI_CURRENT: {AQAPI_CURRENT}"
                f"AQAPI_HOURLY: {AQAPI_HOURLY}"
                f"Unknown Error: {error}"
            )
        return body


class OPENMETEOError(HomeAssistantError):
    """Base error."""


class InvalidAuth(OPENMETEOError):
    """Raised when invalid authentication credentials are provided."""


class APIRatelimitExceeded(OPENMETEOError):
    """Raised when the API rate limit is exceeded."""


class UnknownError(OPENMETEOError):
    """Raised when an unknown error occurs."""
