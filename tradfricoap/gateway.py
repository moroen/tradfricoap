from .config import get_config
from .request import request
from .constants import attr_gateway_reboot, attr_gateway_root

CONF = get_config().configuation

if CONF["Api"] == "Py3coap":
    from .pycoap_api import create_ident
    from .pycoap_api import close_connection

if CONF["Api"] == "Coapcmd":
    from .coapcmd_api import create_ident
    from .coapcmd_api import close_connection


def reboot():
    uri = "{}/{}".format(attr_gateway_root, attr_gateway_reboot)
    return request(uri, payload="1", method="post")
    

