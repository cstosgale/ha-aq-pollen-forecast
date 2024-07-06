"""Pollen Sensor for Home Assistant"""

import logging
from datetime import timedelta, date
from homeassistant.config_entries import ConfigEntry # type: ignore
from homeassistant.const import ( # type: ignore
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
)
from homeassistant.core import HomeAssistant # type: ignore
from homeassistant.helpers.entity import DeviceInfo # type: ignore
from homeassistant.helpers.entity_platform import AddEntitiesCallback # type: ignore
from homeassistant.helpers.aiohttp_client import async_get_clientsession # type: ignore
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType # type: ignore
from homeassistant.components.sensor import ( # type: ignore
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass
)
from homeassistant.helpers.update_coordinator import ( # type: ignore
    CoordinatorEntity,
)

from .const import (
    DOMAIN,
    POLLEN_TYPES,
    GAS_TYPES
)

from .coordinator import OPENMETEOCoordinator

_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(minutes=10)

SENSOR_TYPES = [
    SensorEntityDescription(
        key="alder_pollen",
        name="Curent Alder Pollen",
        icon="mdi:tree"
    ),
    SensorEntityDescription(
        key="birch_pollen",
        name="Curent Birch Pollen",
        icon="mdi:tree"
    ),
    SensorEntityDescription(
        key="grass_pollen",
        name="Curent Grass Pollen",
        icon="mdi:grass"
    ),
    SensorEntityDescription(
        key="mugwort_pollen",
        name="Curent Mugwort Pollen",
        icon="mdi:flower-pollen"
    ),
    SensorEntityDescription(
        key="olive_pollen",
        name="Curent Olive Pollen",
        icon="mdi:tree"
    ),
    SensorEntityDescription(
        key="ragweed_pollen",
        name="Curent Ragweed Pollen",
        icon="mdi:flower-pollen"
    )
]

SENSOR_TYPES = [
    SensorEntityDescription(
        key=key,
        name=f"{"Current"} {details['name']}",
        icon=details["icon"]
    )
    for key, details in POLLEN_TYPES.items()
]

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup sensors from a config entry created in the integrations UI."""  # noqa: D401
    # config = hass.data[DOMAIN][config_entry.entry_id]

    session = async_get_clientsession(hass)
    coordinator = OPENMETEOCoordinator(hass, session, entry.data)

    await coordinator.async_refresh()

    name = "Default Location"
    config_data = entry.data
    pollensensors = [OMPollenSensor(coordinator,
                            name,
                            config_data,
                            description) for description in SENSOR_TYPES
                            if description.key in POLLEN_TYPES]
    gassensors = [OMGasSensor(coordinator,
                            name,
                            config_data,
                            description) for description in SENSOR_TYPES
                            if description.key in GAS_TYPES]
    sensors = pollensensors + gassensors
    async_add_entities(sensors, update_before_add=True)

async def async_setup_platform(
    hass: HomeAssistant,
    entry: ConfigType,
    async_add_entities: AddEntitiesCallback,
    _: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    session = async_get_clientsession(hass)
    coordinator = OPENMETEOCoordinator(hass, session, entry)

    name = "Default Location"

    config_data = entry.data

    sensors = [OMPollenSensor(coordinator,
                            name,
                            config_data,
                            description) for description in SENSOR_TYPES]
    async_add_entities(sensors, update_before_add=True)

class OMBaseSensor(CoordinatorEntity[OPENMETEOCoordinator], SensorEntity):
    """Define an Open Meteo sensor."""

    def __init__(
        self,
        coordinator: OPENMETEOCoordinator,
        name: str,
        config_data: dict,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{name}")},
            name=name,
        )
        self._attr_unique_id = f"{DOMAIN}-{name}-{description.key}".lower()
        self.entity_id = f"sensor.{DOMAIN}_{name}_{description.key}".lower()
        self.entity_description = description
        self._latitude = config_data[CONF_LATITUDE]
        self._longitude = config_data[CONF_LONGITUDE]


    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return bool(self.coordinator.data)

    @property
    def native_value(self) -> str | date | None:
        value = self.coordinator.data["current"][self.entity_description.key] * 1000
        if value and self.entity_description.device_class == SensorDeviceClass.DATE:
            return date.fromisoformat(value)
        return value

class OMPollenSensor(OMBaseSensor):
    """ Pollen Sensor Class"""

    _attr_device_class = SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

class OMGasSensor(OMBaseSensor):
    """ Gas Sensor Class"""

    _attr_device_class = SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
