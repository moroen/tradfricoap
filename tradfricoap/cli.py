import argparse
import json


from .config import get_config
from .errors import HandshakeError
from .device import get_devices, get_device
from .version import get_version_info

from . import ApiNotFoundError

_parser = None

def default_parsers_args():

    global _parser 

    if _parser is None:
        _parser = argparse.ArgumentParser()    
        _parser.add_argument("--debug", action="store_true")

    subparsers = _parser.add_subparsers(dest="command")


    parser_list = subparsers.add_parser("list")
    parser_list.add_argument("--groups", action="store_true")

    subparsers.add_parser("on").add_argument("ID")
    subparsers.add_parser("off").add_argument("ID")

    subparsers.add_parser("version")


    parser_config = subparsers.add_parser("config")
    parser_config_subparser = parser_config.add_subparsers(dest="config")

    parser_config_gateway = parser_config_subparser.add_parser("gw")
    parser_config_gateway.add_argument("IP")
    parser_config_gateway.add_argument("KEY")

    parser_config_api = parser_config_subparser.add_parser("api")
    parser_config_api.add_argument("API", choices=["pycoap", "coapcmd"])
    
    return subparsers

def get_args():
    
    global _parser

    if _parser is None:
        default_parsers_args()

    return _parser.parse_args()

def process_args(args=None):

    if args is None:
        args = get_args()
            
    if args.command == "api":
        print("Command 'api' is deprecated. Did you mean 'config api'")

    if args.command == "config":
        set_config(args)

    elif args.command == "list":
        list_devices(groups=True)

    elif args.command == "on":
        set_state(args.ID, 1)

    elif args.command == "off":
        set_state(args.ID, 0)

    elif args.command == "version":
        info = get_version_info()
        print('\n'.join("{}: {}".format(k, v) for k, v in info.items()), end='')


    else:
        return args




def set_config(args):
    conf_object = get_config()
    

    if args.config == "api":
        conf_object.set_config_item("api", args.API)
        conf_object.save()

    elif args.config == "gw":
        from tradfricoap.gateway import create_ident

        try:
            create_ident(args.IP, args.KEY, conf_object)
        except HandshakeError:
            print("Connection timed out")

    else:
        print(json.dumps(conf_object.configuation, indent=2))



def set_state(id, state):
    device = get_device(id)
    if state not in [0,1]:
        state = 1
    device.State = state


def list_devices(groups=False):
    try:
        devices = get_devices(groups)
    except HandshakeError:
        print("Connection timed out")
        exit()

    except ApiNotFoundError as e:
        # print(e.message)
        raise
        exit()

    if devices is None:
        print("Unable to get list of devices")
    else:
        ikea_devices = []
        plugs = []
        blinds = []
        groups = []
        batteries = []
        others = []

        devices = sorted(devices.items())

        for key, dev in devices:
            if dev.Type == "Light":
                ikea_devices.append(dev.Description)
            elif dev.Type == "Plug":
                plugs.append(dev.Description)
            elif dev.Type == "Blind":
                blinds.append(dev.Description)
            elif dev.Type == "Group":
                groups.append(dev.Description)
            else:
                others.append(dev.Description)

            if dev.Battery_level is not None:
                batteries.append(
                    "{}: {} - {}".format(dev.DeviceID, dev.Name, dev.Battery_level)
                )

        if len(ikea_devices):
            print("Lights:")
            print("\n".join(ikea_devices))

        if len(plugs):
            plugs.sort()
            print("\nPlugs:")
            print("\n".join(plugs))

        if len(blinds):
            blinds.sort()
            print("\nBlinds:")
            print("\n".join(blinds))

        if len(groups):
            groups.sort()
            print("\nGroups:")
            print("\n".join(groups))

        if len(others):
            others.sort()
            print("\nOthers:")
            print("\n".join(others))

        if len(batteries):
            print("\nBatteries:")
            print("\n".join(batteries))