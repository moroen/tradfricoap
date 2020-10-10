import argparse

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

    try:
        from tradfricoap.device import get_devices, get_device
        from tradfricoap.gateway import create_ident
        import tradfricoap.errors as errors
    except ImportError:
        print("Module 'tradfricoap' not found!")
        exit()

    except errors.ApiNotFoundError as e:
        if e.api == "pycoap":
            print('Py3coap module not found!\nInstall with "pip3 install py3coap" or select another api with "tradfri api"')
        elif e.api == "coapcmd":
            print( 'coapcmd  not found!\nInstall with "bash install_coapcmd.sh" or select another api with "tradfri api"')
        exit()

    if args.command == "config":
        from tradfricoap.cli.config import set_config
        set_config(args)

    elif args.command == "list":
        from tradfricoap.cli.devices import list_devices
        list_devices(groups=True)

    elif args.command == "on":
        from tradfricoap.cli.devices import set_state
        set_state(args.ID, 1)

    elif args.command == "off":
        from tradfricoap.cli.devices import set_state
        set_state(args.ID, 0)

    elif args.command == "version":
        from tradfricoap.version import get_version_info
        import pprint

        info = get_version_info()

        print('\n'.join("{}: {}".format(k, v) for k, v in info.items()), end='')


    else:
        return args