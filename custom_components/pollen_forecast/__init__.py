from homeassistant import core
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE

from .sensor import PollenSensor
import const

CONFIG_SCHEMA = vol.Schema({vol.Optional(CONF_LATITUDE): float, vol.Optional(CONF_LONGITUDE): float}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Pollen Sensor component."""
    hass.data[const.DOMAIN] = {}
    hass.data[const.DOMAIN][CONF_LATITUDE] = config.get(CONF_LATITUDE, hass.config.latitude)
    hass.data[const.DOMAIN][CONF_LONGITUDE] = config.get(CONF_LONGITUDE, hass.config.longitude)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Pollen Sensor from a config entry."""
    hass.data[const.DOMAIN]['sensor'] = PollenSensor(hass.data[const.DOMAIN][CONF_LATITUDE], hass.data[const.DOMAIN][CONF_LONGITUDE])
    return True

