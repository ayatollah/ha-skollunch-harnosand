"""Initiering av Skollunch Härnösand."""
from __future__ import annotations

import logging
from datetime import datetime
import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL, BASE_URL

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[str] = ["sensor", "calendar"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Sätt upp integrationen."""
    session = aiohttp.ClientSession()

    async def async_update_data():
        today_str = datetime.now().strftime("%Y-%m-%d")
        data = {}
        try:
            # 1. Hämta dagens rätt
            async with session.get(f"{BASE_URL}?date={today_str}", timeout=10) as r1:
                if r1.status == 200:
                    data["today"] = await r1.json()

            # 2. Hämta morgondagens rätt (eller måndagens vid helg)
            async with session.get(f"{BASE_URL}/tomorrow", timeout=10) as r2:
                if r2.status == 200:
                    data["tomorrow"] = await r2.json()

            # 3. Hämta hela veckans meny
            async with session.get(f"{BASE_URL}/week", timeout=10) as r3:
                if r3.status == 200:
                    data["week"] = await r3.json()

            return data
        except Exception as err:
            raise UpdateFailed(f"Kunde inte synkronisera matsedel: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Skollunch Härnösand",
        update_interval=SCAN_INTERVAL,
        update_method=async_update_data,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "session": session,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Ta bort integrationen."""
    data = hass.data[DOMAIN].pop(entry.entry_id)
    await data["session"].close()
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)