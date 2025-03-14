from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.helpers.event import async_track_time_interval

import logging
from datetime import timedelta

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_PORT,
    CONF_ACCOUNT_ID,
    CONF_SUPERVISION,
    CONF_INTERVAL,
    CONF_SUPERVISION_TS,
    CONF_ACCOUNTS,
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
                    config_entry.data[CONF_SUPERVISION_TS]
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
            service_call.data.get("timestamp"),
            service_call.data.get("message"),
        )

    # async def send_sia_message(service_call: ServiceCall):
    #     """Send a message to the server and in a case of failure, retry by calling supervision"""
    #     message = service_call.data.get("message")
    #     max_attempts = 2

    #     for attempt in range(max_attempts):
    #         current_server_idx = hass.data[DOMAIN].get("connection")
    #         if current_server_idx is None or current_server_idx >= len(accounts):
    #             _LOGGER.error("No valid connection found, starting supervision")
    #             await supervision_message()
    #             current_server_idx = hass.data[DOMAIN].get("connection")
    #             if current_server_idx is None:
    #                 _LOGGER.error("No connection established after supervision")
    #                 return

    #         account = accounts[current_server_idx]
    #         try:
    #             await sia.send_sia(
    #                 account[CONF_HOST],
    #                 account[CONF_PORT],
    #                 account[CONF_ACCOUNT_ID],
    #                 False,
    #                 message,
    #             )
    #             _LOGGER.info(f"Message successfully sent to ")
    #             break  # Succès : on sort de la boucle
    #         except Exception as e:
    #             _LOGGER.error(
    #                 f"Échec de l'envoi sur le compte {current_server_idx} : {e}"
    #             )
    #             # On lance la supervision pour rechercher un autre serveur utilisable
    #             await supervision_message()
    #     else:
    #         _LOGGER.error("Échec de l'envoi du message après plusieurs tentatives.")

    hass.services.async_register(DOMAIN, SERVICE_SEND_SIA_NAME, send_sia_message)

    if config_entry.data[CONF_SUPERVISION]:
        async_track_time_interval(
            hass,
            supervision_message,
            timedelta(seconds=config_entry.data[CONF_INTERVAL]),
        )
        # ExampleServicesSetup(hass, config_entry)
        # await hass.config_entries.async_forward_entry_setups(config_entry, ["binary_sensor"])
        await supervision_message()

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    # return await hass.config_entries.async_unload_platforms(config_entry, ["binary_sensor"])
    return True
