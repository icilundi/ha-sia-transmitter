import logging
import aiohttp

_LOGGER = logging.getLogger(__name__)

async def send_webhook(webhook_url, message_type, sia_data, custom_data):
    #TODO Parse custom data as json before passing it as parameter
    payload = {'type': message_type, 'sia_data': sia_data, **custom_data}
    headers = {"Content-Type": "application/json"}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload, headers=headers, timeout=10) as response:
                response.raise_for_status()
                return True
    except aiohttp.ClientError as e:
        _LOGGER.error(f"Erreur lors de l'envoi du webhook : {e}")
        return False