import argparse

def get_args():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    parser.add_argument("--debug", action="store_true")


    parser_list = subparsers.add_parser("list")
    parser_list.add_argument("--groups", action="store_true")

    subparsers.add_parser("on").add_argument("ID")
    subparsers.add_parser("off").add_argument("ID")

    subparsers.add_parser("test")


    parser_config = subparsers.add_parser("config")
    parser_config_subparser = parser_config.add_subparsers(dest="config")

    parser_config_gateway = parser_config_subparser.add_parser("gw")
    parser_config_gateway.add_argument("IP")
    parser_config_gateway.add_argument("KEY")

    parser_config_api = parser_config_subparser.add_parser("api")
    parser_config_api.add_argument("API", choices=["pycoap", "coapcmd"])
    
    return parser.parse_args()

def process_args():
    args = get_args()

    if args.command == "api":
        config = host_config(CONFIGFILE)    
        config.set_config_item("api", args.API)
        config.save()
        exit()

    try:
        from tradfricoap.device import get_devices, get_device
        from tradfricoap.gateway import create_ident
        import tradfricoap.errors as errors
    except ImportError:
        print("Module 'tradfricoap' not found!")
        exit()

    except ApiNotFoundError as e:
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
    

    else:
        print("Unknown command '{}'".format(args.command))