'''Constants'''

from homeassistant.const import ( # type: ignore
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION
)

DOMAIN = 'aq_pollen_forecast'
AQAPI_URL = 'https://air-quality-api.open-meteo.com/v1/air-quality'

# For the below, tptype determines if the sensor can be used for
# Current and Hourly measurements or just one or the other.

SENSOR_TYPES_DICT = {
    'alder_pollen': {
        'name': 'Alder Pollen',
        'icon': 'mdi:tree',
        'tptype': 'CH',
        'device_class':'VOLATILE_ORGANIC_COMPOUNDS_PARTS',
        'uom': CONCENTRATION_PARTS_PER_MILLION
    },
    'birch_pollen': {
        'name': 'Birch Pollen',
        'icon': 'mdi:tree',
        'tptype': 'CH',
        'device_class':'VOLATILE_ORGANIC_COMPOUNDS_PARTS',
        'uom': CONCENTRATION_PARTS_PER_MILLION
    },
    'grass_pollen': {
        'name': 'Grass Pollen',
        'icon': 'mdi:grass',
        'tptype': 'CH',
        'device_class':'VOLATILE_ORGANIC_COMPOUNDS_PARTS',
        'uom': CONCENTRATION_PARTS_PER_MILLION
    },
    'mugwort_pollen': {
        'name': 'Mugwort Pollen',
        'icon': 'mdi:flower-pollen',
        'tptype': 'CH',
        'device_class':'VOLATILE_ORGANIC_COMPOUNDS_PARTS',
        'uom': CONCENTRATION_PARTS_PER_MILLION
    },
    'olive_pollen': {
        'name': 'Olive Pollen',
        'icon': 'mdi:tree',
        'tptype': 'CH',
        'device_class':'VOLATILE_ORGANIC_COMPOUNDS_PARTS',
        'uom': CONCENTRATION_PARTS_PER_MILLION
    },
    'ragweed_pollen': {
        'name': 'Ragweed Pollen',
        'icon': 'mdi:flower-pollen',
        'tptype': 'CH',
        'device_class':'VOLATILE_ORGANIC_COMPOUNDS_PARTS',
        'uom': CONCENTRATION_PARTS_PER_MILLION
    },
    'european_aqi': {
        'name': 'European Aqi',
        'icon': 'mdi:air-filter',
        'tptype': 'C',
        'device_class':'AQI',
        'uom': ''
    },
    'us_aqi': {
        'name': 'Us Aqi',
        'icon': 'mdi:air-filter',
        'tptype': 'C',
        'device_class':'AQI',
        'uom': ''
    },
    'pm10': {
        'name': 'Pm10',
        'icon': 'mdi:blur',
        'tptype': 'CH',
        'device_class':'PM10',
        'uom': CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    },
    'pm2_5': {
        'name': 'Pm2 5',
        'icon': 'mdi:blur',
        'tptype': 'CH',
        'device_class':'PM25',
        'uom': CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    },
    'carbon_monoxide': {
        'name': 'Carbon Monoxide',
        'icon': 'mdi:molecule-co',
        'tptype': 'CH',
        'device_class':'VOLATILE_ORGANIC_COMPOUNDS',
        'uom': CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    },
    'nitrogen_dioxide': {
        'name': 'Nitrogen Dioxide',
        'icon': 'mdi:molecule',
        'tptype': 'CH',
        'device_class':'VOLATILE_ORGANIC_COMPOUNDS',
        'uom': CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    },
    'sulphur_dioxide': {
        'name': 'Sulphur Dioxide',
        'icon': 'mdi:molecule',
        'tptype': 'CH',
        'device_class':'VOLATILE_ORGANIC_COMPOUNDS',
        'uom': CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    },
    'ozone': {
        'name': 'Ozone',
        'icon': 'mdi:cloud-circle',
        'tptype': 'CH',
        'device_class':'VOLATILE_ORGANIC_COMPOUNDS',
        'uom': CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    },
    'aerosol_optical_depth': {
        'name': 'Aerosol Optical Depth',
        'icon': 'mdi:weather-fog',
        'tptype': 'CH',
        'device_class':'',
        'uom': ''
    },
    'dust': {
        'name': 'Dust',
        'icon': 'mdi:weather-dust',
        'tptype': 'CH',
        'device_class':'VOLATILE_ORGANIC_COMPOUNDS',
        'uom': CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    },
    'uv_index': {
        'name': 'UV Index',
        'icon': 'mdi:weather-sunny',
        'tptype': 'CH',
        'device_class':'',
        'uom': ''
    },
    'uv_index_clear_sky': {
        'name': 'UV Index Clear Sky',
        'icon': 'mdi:weather-sunny-alert',
        'tptype': 'CH',
        'device_class':'',
        'uom': ''
    }
}

AQAPI_CURRENT = ','.join(
    [key for key, value in SENSOR_TYPES_DICT.items() if 'C' in value['tptype']]
    )
AQAPI_HOURLY = ','.join(
    [key for key, value in SENSOR_TYPES_DICT.items() if 'H' in value['tptype']]
    )
