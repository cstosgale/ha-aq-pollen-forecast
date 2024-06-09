"""Config flow for Pollen Forecast integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# TODO adjust the data schema to the data that you need


class ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pollen Forecast."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors: dict[str, str] = {}
        hass_latitude = self.hass.config.latitude
        hass_longitude = self.hass.config.longitude

        DATA_SCHEMA = vol.Schema(
            {
                vol.Required(CONF_LATITUDE, default=hass_latitude): float,
                vol.Required(CONF_LONGITUDE, default=hass_longitude): float,
            }
        )
        if user_input is not None:
            return self.async_create_entry(title="Pollen Forecast", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
