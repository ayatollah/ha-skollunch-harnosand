"""Config flow för Skollunch Härnösand."""
from __future__ import annotations

from homeassistant import config_entries
from .const import DOMAIN


class SkollunchConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Enkelt flöde utan formulärfält."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Installera direkt med ett klick."""
        await self.async_set_unique_id("skollunch_harnosand_singleton")
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(title="Skollunch Härnösand", data={})

        return self.async_show_form(step_id="user")