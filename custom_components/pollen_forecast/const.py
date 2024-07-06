"""Constants"""

DOMAIN = "pollen_forecast"
AQAPI_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
POLLEN_TYPES = [
    "alder_pollen",
    "birch_pollen",
    "grass_pollen",
    "mugwort_pollen",
    "olive_pollen",
    "ragweed_pollen"
    ]
AQI_TYPES = ["european_aqi","us_aqi"]
PM10 = "pm10"
PM2_5= "pm2_5"
GAS_TYPES=["carbon_monoxide",
           "nitrogen_dioxide",
           "sulphur_dioxide",
           "ozone",
           "aerosol_optical_depth",
           "dust"]
UV_INDEX_TYPES=["uv_index","uv_index_clear_sky"]
AQAPI_CURRENT = ",".join([",".join(AQI_TYPES),
                          PM10,PM2_5,
                          ",".join(GAS_TYPES),",".join(UV_INDEX_TYPES),
                          ",".join(POLLEN_TYPES)])
AQAPI_HOURLY = ",".join([PM10,PM2_5,
                         ",".join(GAS_TYPES),
                         ",".join(UV_INDEX_TYPES),
                         ",".join(POLLEN_TYPES)])
