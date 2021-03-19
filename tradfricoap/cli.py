import argparse
import json
from os import close

from . import ApiNotFoundError

_global_error = None

try:
    from .errors import (
        HandshakeError,
        DeviceNotFoundError,
        UriNotFoundError,
        MethodNotAllowedError,
        ReadTimeoutError,
        WriteTimeoutError,
        GatewayNotSpecified,
    )
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

    name = subparsers.add_parser("name")
    name.add_argument("ID")
    name.add_argument("name")

    raw = subparsers.add_parser("raw")
    raw.add_argument("ID")
    raw.add_argument("--plain", action="store_true")
    raw.add_argument("--indent", default=2)

    version_parser = subparsers.add_parser("version")
    version_parser.add_argument("-s", "--short", action="store_true")

    subparsers.add_parser("reboot")

    subparsers.add_parser("test")

    # uri
    get = subparsers.add_parser("get")
    get.add_argument("uri")

    put = subparsers.add_parser("put")
    put.add_argument("uri")
    put.add_argument("payload")

    post = subparsers.add_parser("post")
    post.add_argument("uri")
    post.add_argument("payload")

    # Server
    server = subparsers.add_parser("server")

    # Config
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

        if args.short:
            print(info["Tradfricoap"])
        else:
            print("\n".join("{}: {}".format(k, v) for k, v in info.items()), end="")
    
        return

    elif args.command == "test":
        print("Do test")
        
    if _global_error is not None:
        print(_global_error)
        return

    if args.command == "server":
        from tradfricoap.server import run_server
        run_server()

    try:
        if args.command == "get":
            from .request import request

            res = request(args.uri)
            print(res)

        if args.command == "put":
            from .request import request

            res = request(args.uri, payload=args.payload, method="put")
            print(res)

        if args.command == "post":
            from .request import request

            res = request(args.uri, payload=args.payload, method="post")
            print(res)
    except UriNotFoundError:
        print("Error: {} not found!".format(args.uri))
        exit()
    except MethodNotAllowedError:
        print("Error: Method {} not supported for {}".format(args.command, args.uri))
        exit()
    except GatewayNotSpecified:
        print("Error: Gateway not specified!")
        exit()


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

        elif args.command == "name":
            device.Name = args.name
            print(device.Description)

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
    except (ApiNotFoundError) as e:
        print(e.message)

    except (HandshakeError):
        print("Connection timed out.")
    
    except GatewayNotSpecified:
        print("Error: Gateway not specified!")
        exit()

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
        try:
            from tradfricoap.gateway import create_ident
        except ModuleNotFoundError:
            # Locally installed
            from .gateway import create_ident

        try:
            create_ident(args.IP, args.KEY, conf_object)
        except HandshakeError:
            print("Connection timed out")

    else:
        print(json.dumps(conf_object.configuation, indent=2))

def list_devices(groups=False):
    try:
        from .device import get_sorted_devices
        ikea_devices, plugs, blinds, groups, others, batteries = get_sorted_devices(groups)    

    except HandshakeError:
        print("Connection timed out")
        exit()

    except ReadTimeoutError:
        print("COAP Read timed out")
        exit()

    except ApiNotFoundError:
        raise

    if len(ikea_devices):
        print("Lights:")
        for dev in ikea_devices:
            print("{}".format(dev.Description))

    if len(plugs):
        print("\nPlugs:")
        for dev in plugs:
            print("{}".format(dev.Description))

    if len(blinds):
        print("\nBlinds:")
        for dev in blinds:
            print("{}".format(dev.Description))

    if len(groups):
        print("\nGroups:")
        for dev in groups:
            print("{}".format(dev.Description))

    if len(batteries):
        print("\nBatteries:")
        for dev in batteries:
            print("{}".format(dev.Description))

    if len(others):
        print("\nOther:")
        for dev in others:
            print("{}".format(dev.Description))

    