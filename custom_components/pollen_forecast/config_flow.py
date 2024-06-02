from homeassistant import config_entries
import voluptuous as vol
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from .const import DOMAIN

class MyCustomComponentConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        # Retrieve the latitude and longitude from the Home Assistant core configuration
        hass_latitude = self.hass.config.latitude
        hass_longitude = self.hass.config.longitude

        # Set the default values in the form
        data_schema = vol.Schema({
            vol.Required(CONF_LATITUDE, default=hass_latitude): float,
            vol.Required(CONF_LONGITUDE, default=hass_longitude): float
        })

        if user_input is not None:
            # Save the input and create the config entry
            return self.async_create_entry(title='Pollen Forecast', data=user_input)

        return self.async_show_form(step_id='user', data_schema=data_schema)
