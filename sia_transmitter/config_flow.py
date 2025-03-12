"""Config flow for sia integration."""

from __future__ import annotations

import logging
from typing import Any
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
)

from homeassistant.const import CONF_PORT, CONF_PROTOCOL

from .const import (
    CONF_HOST,
    CONF_ACCOUNT_ID,
    CONF_ACCOUNTS,
    CONF_ADDITIONAL_ACCOUNTS,
    CONF_INTERVAL,
    DOMAIN,
    TITLE,
)

_LOGGER = logging.getLogger(__name__)

MAIN_ACCOUNT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT): int,
        # vol.Optional(CONF_PROTOCOL, default="TCP"): vol.In(["TCP", "UDP"]),
        vol.Required(CONF_ACCOUNT_ID): str,
        # vol.Optional(CONF_ENCRYPTION_KEY): str,
        vol.Required(CONF_INTERVAL, default=1): int,
        vol.Optional(CONF_ADDITIONAL_ACCOUNTS, default=False): bool,
    }
)

ACCOUNT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT): int,
        # vol.Optional(CONF_PROTOCOL, default="TCP"): vol.In(["TCP", "UDP"]),
        vol.Required(CONF_ACCOUNT_ID): str,
        # vol.Optional(CONF_ENCRYPTION_KEY): str,
        vol.Optional(CONF_ADDITIONAL_ACCOUNTS, default=False): bool,
    }
)

class SIAConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for sia."""

    VERSION: int = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._data: dict[str, Any] = {CONF_INTERVAL : 0, CONF_ACCOUNTS: []}
        # self._options: Mapping[str, Any] = {CONF_ACCOUNTS: {}}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial user step."""
        errors: dict[str, str] | None = None
        if user_input is not None:
            pass
            # errors = validate_input(user_input)
        if user_input is None or errors is not None:
            return self.async_show_form(
                step_id="user", data_schema=MAIN_ACCOUNT_SCHEMA, errors=errors
            )
        return await self.async_handle_data_and_route(user_input)

    async def async_step_add_account(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the additional accounts steps."""
        errors: dict[str, str] | None = None
        if user_input is not None:
            # errors = validate_input(user_input)
            pass
        if user_input is None or errors is not None:
            return self.async_show_form(
                step_id="add_account", data_schema=ACCOUNT_SCHEMA, errors=errors
            )
        return await self.async_handle_data_and_route(user_input)

    async def async_handle_data_and_route(
        self, user_input: dict[str, Any]
    ) -> ConfigFlowResult:
        """Handle the user_input, check if configured and route to the right next step or create entry."""
        if user_input.get(CONF_INTERVAL):
            self._data[CONF_INTERVAL] = user_input[CONF_INTERVAL]
        
        self._data[CONF_ACCOUNTS].append(
            {
                CONF_HOST: user_input[CONF_HOST],
                CONF_PORT: user_input[CONF_PORT],
                CONF_ACCOUNT_ID: user_input[CONF_ACCOUNT_ID],
            }
        )

        if user_input[CONF_ADDITIONAL_ACCOUNTS]:
            return await self.async_step_add_account()
        return self.async_create_entry(
            title=TITLE.format(self._data[CONF_ACCOUNTS][0][CONF_PORT]),
            data=self._data,
        )
