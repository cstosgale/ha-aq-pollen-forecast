"""Pollen Sensor for Home Assistant"""

import logging
from datetime import datetime, timedelta, date
from homeassistant.config_entries import ConfigEntry # type: ignore
from homeassistant.exceptions import HomeAssistantError # type: ignore
from homeassistant.const import ( # type: ignore
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
)
from homeassistant.core import HomeAssistant # type: ignore
from homeassistant.helpers.entity import DeviceInfo # type: ignore
from homeassistant.helpers.entity_platform import AddEntitiesCallback # type: ignore
from homeassistant.helpers.aiohttp_client import async_get_clientsession # type: ignore
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
    SENSOR_TYPES_DICT
)

from .coordinator import OPENMETEOCoordinator

_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(minutes=10)

# Create a list of all Current Sensors
SENSOR_TYPES = [
    SensorEntityDescription(
        key=key,
        name=f"{"Current"} {value['name']}",
        icon=value["icon"]
    )
    for key, value in SENSOR_TYPES_DICT.items() if "C" in value["tptype"]
]

# Create a list of all Forecast Sensors. This includes 0 for today's Forecast.
for i in range(4):
    SENSOR_TYPES = SENSOR_TYPES + [
        SensorEntityDescription(
            key=key,
            name=f"{value['name']} {i}d",
            icon=value["icon"]
        )
        for key, value in SENSOR_TYPES_DICT.items() if "H" in value["tptype"]
    ]

def get_max_value_for_date(data, key, tptype):
    """Function to get the maximum value from the forecast data for the following days"""
    # N.B. Expects tptype to follow the format H1, H2, or H3
    # with the number denoting the forecasted day

    # Extract the time and grass pollen values
    times = data["hourly"]["time"]
    values = data["hourly"][key]

    # Get Target date based on provided value:
    target_date = (datetime.now() + timedelta(days=int(tptype [0]))).strftime("%Y-%m-%d")
    # Filter the grass pollen values for the target date
    filtered_values = [
        values[i] for i in range(len(times)) if times[i].startswith(target_date)
    ]

    # Calculate the maximum value for the target date
    try:
        max_value = max(filtered_values)
    except ValueError as err:
        err_str = str(err)
        _LOGGER.exception("Issue calculating max value for %s. error: %s", key, err_str)
        raise UnknownError from err

    return max_value

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup sensors from a config entry created in the integrations UI."""  # noqa: D401

    session = async_get_clientsession(hass)
    coordinator = OPENMETEOCoordinator(hass, session, entry.data)

    await coordinator.async_refresh()

    name = "Home"

    config_data = entry.data

    # Create a list of the sensors to create
    # each one using the correct class based on the class defined in the dictionary
    sensors = []
    for key, value in SENSOR_TYPES_DICT.items():
        # Get a class object for the name of the class value in the dictionary
        # class_obj = getattr(sys.modules[__name__], value["class"])
        sensor = [OMBaseSensor(coordinator,
                        name,
                        config_data,
                        value["device_class"],
                        value["uom"],
                        description

            ) for description in SENSOR_TYPES if description.key == key]
        sensors = sensors + sensor

    async_add_entities(sensors, update_before_add=True)

class OMBaseSensor(CoordinatorEntity[OPENMETEOCoordinator], SensorEntity):
    """Define an Open Meteo sensor."""

    def __init__(
        self,
        coordinator: OPENMETEOCoordinator,
        name: str,
        config_data: dict,
        device_class: str,
        uom: str,
        description: SensorEntityDescription
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{name}")},
            name=name,
        )
        self._attr_unique_id = f"{DOMAIN}-{name}-{description.name.replace(" ","-")}".lower()
        self.entity_id = f"sensor.{name}_{description.name.replace(" ","_")}".lower()
        self.entity_description = description
        self._name = description.name
        self._latitude = config_data[CONF_LATITUDE]
        self._longitude = config_data[CONF_LONGITUDE]
        if device_class != '':
            self._attr_device_class = getattr(SensorDeviceClass, device_class)
        self._attr_state_class = SensorStateClass.MEASUREMENT
        if uom != '':
            self._attr_native_unit_of_measurement = uom

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return bool(self.coordinator.data)

    @property
    def native_value(self) -> str | date | None:
        if self._name.startswith("Current"):
            value = self.coordinator.data["current"][self.entity_description.key]
        elif self._name.endswith("d"):
            value = get_max_value_for_date(
                self.coordinator.data,
                self.entity_description.key,
                self._name[-2:]
                )
        else:
            _LOGGER.warning(
                "Sensor with name %s has invalid name and will have no value", self._name
                )
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

class OMAQISensor(OMBaseSensor):
    """ AQI Sensor Class"""

    _attr_device_class = SensorDeviceClass.AQI
    _attr_state_class = SensorStateClass.MEASUREMENT

class OMSensor(OMBaseSensor):
    """ Gas Sensor Class"""

    _attr_device_class = SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

class OPENMETEOError(HomeAssistantError):
    """Base error."""

class UnknownError(OPENMETEOError):
    """Raised when an unknown error occurs."""
