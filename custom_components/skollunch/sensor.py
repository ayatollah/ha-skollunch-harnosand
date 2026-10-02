"""Sensorer för Skollunch Härnösand."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

SCHOOL_CONFIGS = [
    {
        "id": "grundskola",
        "name": "Skollunch Grundskola",
        "icon": "mdi:food-apple",
    },
    {
        "id": "gymnasium",
        "name": "Skollunch Gymnasium",
        "icon": "mdi:food-drumstick",
    },
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Initiera sensorer."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([
        SkollunchSchoolSensor(coordinator, entry, cfg) for cfg in SCHOOL_CONFIGS
    ])


class SkollunchSchoolSensor(CoordinatorEntity, SensorEntity):
    """Sensor för en skolas meny."""

    def __init__(self, coordinator, entry: ConfigEntry, cfg: dict) -> None:
        super().__init__(coordinator)
        self._school_id = cfg["id"]
        self._attr_unique_id = f"skollunch_{self._school_id}"
        self._attr_name = cfg["name"]
        self._attr_icon = cfg["icon"]

    @property
    def native_value(self) -> str:
        """Dagens huvudrätt."""
        data = self.coordinator.data or {}
        today_data = data.get("today", {}).get(self._school_id)
        if today_data and "dish" in today_data:
            return today_data["dish"]
        return "Ingen skollunch idag"

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Extra information för automationer och dashboards."""
        data = self.coordinator.data or {}
        today_data = data.get("today", {}).get(self._school_id) or {}
        tomorrow_data = data.get("tomorrow", {}).get(self._school_id) or {}
        week_data = data.get("week", {}).get(self._school_id) or []

        return {
            "alt_dish": today_data.get("altDish"),
            "tomorrow_dish": tomorrow_data.get("dish", "Ingen skollunch imorgon"),
            "tomorrow_alt_dish": tomorrow_data.get("altDish"),
            "tomorrow_date": data.get("tomorrow", {}).get("date"),
            "week_menu": week_data,
            "week_number": data.get("week", {}).get("weekNumber"),
            "school_type": self._school_id,
            "updated_at": data.get("today", {}).get("updatedAt"),
        }