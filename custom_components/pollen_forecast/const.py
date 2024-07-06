"""Constants"""

DOMAIN = "pollen_forecast"
AQAPI_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
POLLEN_TYPES = {
    "alder_pollen": {"name": "Alder Pollen", "icon": "mdi:tree", "tp": "current"},
    "birch_pollen": {"name": "Birch Pollen", "icon": "mdi:tree", "tp": "current"},
    "grass_pollen": {"name": "Grass Pollen", "icon": "mdi:grass", "tp": "current"},
    "mugwort_pollen": {"name": "Mugwort Pollen", "icon": "mdi:flower-pollen", "tp": "current"},
    "olive_pollen": {"name": "Olive Pollen", "icon": "mdi:tree", "tp": "current"},
    "ragweed_pollen": {"name": "Ragweed Pollen", "icon": "mdi:flower-pollen", "tp": "current"}
}
AQI_TYPES = ["european_aqi","us_aqi"]
PM_TYPES = ["pm10", "pm2_5"]
GAS_TYPES=["carbon_monoxide",
           "nitrogen_dioxide",
           "sulphur_dioxide",
           "ozone",
           "aerosol_optical_depth",
           "dust"]
UV_INDEX_TYPES=["uv_index","uv_index_clear_sky"]
AQAPI_CURRENT = ",".join(
    [
        ",".join(AQI_TYPES),
        ",".join(PM_TYPES),
        ",".join(GAS_TYPES),
        ",".join(UV_INDEX_TYPES),
        ",".join(POLLEN_TYPES.keys())
        ]
    )
AQAPI_HOURLY = ",".join(
    [
        ",".join(PM_TYPES),
        ",".join(GAS_TYPES),
        ",".join(UV_INDEX_TYPES),
        ",".join(POLLEN_TYPES.keys())
        ]
    )
