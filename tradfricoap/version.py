import pkg_resources, subprocess
from .coapcmd_api import get_version, set_coapcmd

def get_version_info():
    try:
        tradfricoap_version = pkg_resources.get_distribution('tradfricoap').version
    except pkg_resources.DistributionNotFound:
        tradfricoap_version = "Not found"

    try:
        py3coap_version = pkg_resources.get_distribution('py3coap').version
    except pkg_resources.DistributionNotFound:
        py3coap_version = "Not found"

    return {"Tradfricoap": tradfricoap_version, "Py3coap": py3coap_version, "coapcmd": get_version()}