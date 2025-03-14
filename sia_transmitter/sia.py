import voluptuous as vol
import logging
import socket
from datetime import datetime, timezone

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse, callback
from .const import (
    DOMAIN,
    CONF_ACCOUNTS,
    CONF_HOST,
    CONF_PORT,
    CONF_ACCOUNT_ID,
    SERVICE_SEND_SIA_NAME,
)

_LOGGER = logging.getLogger(__name__)


class SIAError(Exception):
    """Generic error for SIA communication"""

    pass


class ConnectionError(SIAError):
    """Error while establishing connection"""

    pass


class ResponseError(SIAError):
    """Error contained in the SIA response from the server"""

    pass


class SIAProtocol:
    """Class to handle sending message using SIA protocol"""
    seq_number = 1

    def get_seq_number(self):
        return str(self.seq_number).zfill(4)
    
    def add_to_seq(self):
        if self.seq_number == 9999:
            self.seq_number = 1
            return
        self.seq_number += 1

    async def send_sia(
        self, host: str, port: int, account_id: str, timestamp: bool, data: str = "", extended_data: str = ""
    ) -> None:
        ts = f"_{datetime.now(timezone.utc).strftime('%H:%M:%S,%m-%d-%Y')}" if timestamp else ""
        ext_data = f"[{extended_data}]" if extended_data else ""
        message = f'"SIA-DCS"{self.get_seq_number()}L0#{account_id}[{data}]{ext_data}{ts}'
        message_length = self._change_hex_format(hex(len(message)))
        crc = self._crc_calc(message)
        sia_message = f"\x0A{crc}{message_length}{message}\x0D"
        _LOGGER.warning({sia_message})
        # Create a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # Connect to Home Assistant SIA server
                sock.connect((host, port))
                _LOGGER.warning(f"Connected to {host}:{port}")

                # Send the message
                sock.sendall(sia_message.encode())
                _LOGGER.warning("SIA Message sent!")

                # Receive acknowledgment (optional, if HA responds)
                response = sock.recv(1024)
                response_message = response.decode()

                if "ACK" not in response_message:
                    raise ResponseError(f"Server did not return an acknowledgement: {response.decode()}")
                
                self.add_to_seq()

            except socket.timeout as e:
                raise ConnectionError(
                    f"Timeout while trying to connect to {host}:{port}"
                ) from e
            except socket.error as e:
                raise ConnectionError(
                    f"Socket error while trying to connect to {host}:{port}: {e}"
                ) from e
            except Exception as e:
                raise ConnectionError(
                    f"Error while trying to connect to {host}:{port}: {e}"
                ) from e
            finally:
                # Close the connection
                sock.close()

    @staticmethod
    def _crc_calc(msg: str | None) -> str | None:
        """Calculate the CRC of the msg."""
        if msg is None:
            return None
        crc = 0
        for letter in str.encode(msg):
            temp = letter
            for _ in range(0, 8):
                temp ^= crc & 1
                crc >>= 1
                if (temp & 1) != 0:
                    crc ^= 0xA001
                temp >>= 1
        return ("%x" % crc).upper().zfill(4)

    @staticmethod
    def _change_hex_format(temp: str | None) -> str | None:
        """Remove 0x in the hex and force it on a 2 bytes format."""
        if temp is None:
            return None
        temp = temp[2:]
        return temp.zfill(4)
