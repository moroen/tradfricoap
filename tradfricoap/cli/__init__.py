import argparse

from tradfricoap.config import get_config, host_config
from tradfricoap import ApiNotFoundError
from tradfricoap.errors import HandshakeError

from .args import get_args, process_args

