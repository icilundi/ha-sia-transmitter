from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.helpers.event import async_track_time_interval

import logging
from datetime import timedelta

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_ACCOUNTS,
    CONF_ACCOUNT_ID,
    CONF_PORT,
    CONF_INTERVAL,
    SERVICE_SEND_SIA_NAME,
)
from .sia import SIAProtocol

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault("connection", 0)
    accounts = config_entry.data[CONF_ACCOUNTS]
    sia = SIAProtocol()

    async def supervision_message(*_args):
        for idx, account in enumerate(accounts):
            try:
                await sia.send_sia(
                    account[CONF_HOST],
                    account[CONF_PORT],
                    account[CONF_ACCOUNT_ID],
                    True,
                )
                hass.data[DOMAIN]["connection"] = idx
                _LOGGER.warning(f"Connexion réussie avec le compte à l'index {idx}.")
                break
            except Exception as e:
                _LOGGER.error(f"Échec de connexion pour le compte {idx}: {e}")
                continue

    async def send_sia_message(service_call: ServiceCall):
        current_server = hass.data[DOMAIN]["connection"]
        account = accounts[current_server]
        await sia.send_sia(
            account[CONF_HOST],
            account[CONF_PORT],
            account[CONF_ACCOUNT_ID],
            False,
            service_call.data.get("message"),
        )

    hass.services.async_register(DOMAIN, SERVICE_SEND_SIA_NAME, send_sia_message)

    async_track_time_interval(
        hass, supervision_message, timedelta(seconds=config_entry.data[CONF_INTERVAL])
    )
    # ExampleServicesSetup(hass, config_entry)
    # await hass.config_entries.async_forward_entry_setups(config_entry, ["binary_sensor"])

    await supervision_message()
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    # return await hass.config_entries.async_unload_platforms(config_entry, ["binary_sensor"])
    return True
