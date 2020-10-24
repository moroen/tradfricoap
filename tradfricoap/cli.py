import argparse
import json

from . import ApiNotFoundError

_global_error = None

try:
    from .config import get_config
    from .errors import HandshakeError, DeviceNotFoundError
    from .device import get_devices, get_device
except ApiNotFoundError as e:
    _global_error = e.message

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

    level = subparsers.add_parser("level")
    level.add_argument("ID")
    level.add_argument("level")
    
    raw = subparsers.add_parser("raw")
    raw.add_argument("ID")
    raw.add_argument("--plain", action="store_true")
    raw.add_argument("--indent", default=2)

    subparsers.add_parser("version")
    
    subparsers.add_parser("reboot")
    

    parser_config = subparsers.add_parser("config")
    parser_config_subparser = parser_config.add_subparsers(dest="config")

    parser_config_gateway = parser_config_subparser.add_parser("gw")
    parser_config_gateway.add_argument("IP")
    parser_config_gateway.add_argument("KEY")

    parser_config_api = parser_config_subparser.add_parser("api")
    parser_config_api.add_argument("API", choices=["py3coap", "coapcmd"])
    
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
        return

    elif args.command == "config":
        set_config(args)
        return

    elif args.command == "version":
        from .version import get_version_info
        info = get_version_info()
        print('\n'.join("{}: {}".format(k, v) for k, v in info.items()), end='')
        return

    if _global_error is not None:
        print(_global_error)
        return

    try:
        if "ID" in args:
            try:
                device = get_device(args.ID)
            except DeviceNotFoundError:
                print("Device with id '{}' not found".format(args.ID))
                exit()

        if args.command == "list":
            list_devices(groups=True)

        elif args.command == "on":
            device.State = 1

        elif args.command == "off":
            device.State = 0

        elif args.command == "level":
            if validate_range(int(args.level)):
                device.Level = int(args.level)
            else:
                show_error("Level outside permitted range (0 - 254)")

        elif args.command == "reboot":
            from .gateway import reboot
            reboot()

        elif args.command == "raw":
            if args.plain:
                print(device.device)
            else:
                
                print(json.dumps(device.device, indent=int(args.indent)))

        else:
            return args
    except ApiNotFoundError as e:
        print(e.message)
        
def show_error(msg):
    print("Error: {}".format(msg))

def validate_range(value, min=0, max=254):
    return min <= value <= max

def set_config(args):
    from .config import get_config
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