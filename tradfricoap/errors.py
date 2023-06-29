from .config import get_config
from . import ApiNotFoundError

_debug = 0

CONF = get_config().configuration

if CONF["Api"] == "Py3coap":
    try:
        from .pycoap_api import (
            HandshakeError,
            UriNotFoundError,
            ReadTimeoutError,
            WriteTimeoutError,
            MethodNotAllowedError,
            set_debug_level,
        )
    except ImportError:
        raise ApiNotFoundError("py3coap", "py3coap not found")

if CONF["Api"] == "Coapcmd":
    try:
        from .coapcmd_api import (
            HandshakeError,
            UriNotFoundError,
            ReadTimeoutError,
            WriteTimeoutError,
            MethodNotAllowedError,
            set_debug_level,
        )
    except ImportError:
        raise


class DeviceNotFoundError(Exception):
    def __init__(self, deviceid):
        self.DeviceID = deviceid

class GatewayNotSpecified(Exception):
    pass