
from tradfricoap.config import get_config
from tradfricoap.errors import HandshakeError
import json

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
