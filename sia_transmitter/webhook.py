import requests

def send_webhook(webhook_url, message_type, sia_data, custom_data):
    payload = {'type':webhook_type, **sia_data, **custom_data}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(webhook_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        _LOGGER.error(f"Erreur lors de l'envoi du webhook : {e}")
