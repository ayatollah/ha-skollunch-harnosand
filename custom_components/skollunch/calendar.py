"""Kalenderplattform för Skollunch Härnösand."""
from __future__ import annotations

from datetime import datetime, date, timedelta
from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Sätt upp kalenderentiteter."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async_add_entities([
        SkollunchCalendar(coordinator, entry, "grundskola", "Skollunch Grundskola Kalender"),
        SkollunchCalendar(coordinator, entry, "gymnasium", "Skollunch Gymnasium Kalender"),
    ])


class SkollunchCalendar(CoordinatorEntity, CalendarEntity):
    """Representerar skolmenyn i kalendern."""

    def __init__(self, coordinator, entry: ConfigEntry, school_id: str, name: str) -> None:
        super().__init__(coordinator)
        self._school_id = school_id
        self._attr_unique_id = f"skollunch_calendar_{school_id}"
        self._attr_name = name

    @property
    def event(self) -> CalendarEvent | None:
        """Nästa kommande måltidshändelse."""
        events = self._get_events()
        now = date.today()
        for ev in events:
            if ev.start >= now:
                return ev
        return events[0] if events else None

    def _get_events(self) -> list[CalendarEvent]:
        data = self.coordinator.data or {}
        week_items = data.get("week", {}).get(self._school_id) or []
        events = []

        for item in week_items:
            date_str = item.get("date")
            if not date_str:
                continue
            try:
                ev_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                desc = f"Huvudrätt: {item.get('dish')}"
                if item.get("altDish"):
                    desc += f"\nVegetariskt: {item.get('altDish')}"

                events.append(
                    CalendarEvent(
                        start=ev_date,
                        end=ev_date + timedelta(days=1),
                        summary=item.get("dish", "Skollunch"),
                        description=desc,
                    )
                )
            except ValueError:
                continue

        return events

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Returnera händelser inom angivet tidsintervall."""
        events = self._get_events()
        start = start_date.date()
        end = end_date.date()
        return [ev for ev in events if start <= ev.start <= end]