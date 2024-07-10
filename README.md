# Air Quality and Pollen Forecast for Home Assistant

This custom component for Home Assistant provides Air Quality and Pollen Data from https://open-meteo.com/en/docs/air-quality-api.

Sensors are created for all available measurements from the API, as follows:

- Current Sensors: Sensors displaying the curent reading for your location
- Forecast Sensors: Sensors ending 0-3d providing todays and 3 following days forecast. These take the maximum value for each day and report that as the forecast.

Correct units are defined for each measurement, although please note that Parts per Metre Squared (which is the correct unit for pollen) is not available in Home Assistant, so Parts Per Million (PPM) which has the same abreviation is used.

## Installation

1. In HACS, add https://github.com/cstosgale/ha-aq-pollen-forecast as a custom repository
2. Add the integration. By default the co-ordinates from your Home Assistant installation will be used, but this can be changed as desired.
