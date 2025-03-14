from typing import Final

DOMAIN : Final = "sia_transmitter"
TITLE : Final = "SIA Alarm on port {}"
CONF_HOST : Final = "host" # Can be removed and use home assistant built in instead
CONF_PORT : Final = "port" # Can be removed and use home assistant built in instead
CONF_ACCOUNT_ID : Final = "account_id"
CONF_SUPERVISION : Final = "enable_supervision"
CONF_INTERVAL : Final = "interval"
CONF_SUPERVISION_TS : Final = "supervision_timestamp"
CONF_ADDITIONAL_ACCOUNTS : Final = "additional_account"
CONF_ACCOUNTS : Final = "accounts"
CONF_ACCOUNT : Final = "account"
SERVICE_SEND_SIA_NAME : Final = "service_send_sia"