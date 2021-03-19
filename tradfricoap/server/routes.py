import os
from string import Template
from json import dumps

from urllib.parse import parse_qs, parse_qsl

from .request_response import request_response, _content_json
from ..errors import HandshakeError
from ..config import get_config

routes = {"GET": {}, "POST": {}, "OPTIONS": {}}

class url(object):
    @staticmethod
    def GET(name):
        def wrapper(f):
            routes["GET"][name] = f
            return f

        return wrapper

    @staticmethod
    def POST(name):
        def wrapper(f):
            routes["POST"][name] = f
            return f

        return wrapper

    @staticmethod
    def OPTIONS(name):
        def wrapper(f):
            routes["OPTIONS"][name] = f
            return f

        return wrapper


def get_post_data(request):
    return dict(parse_qsl(request["Data"].decode("utf-8")))

@url.GET("/status")
def get_status(request):
    from ..request import request
    from ..constants import uriDevices

    request(uriDevices)
    
    return request_response(status=200, response=dumps({"Command": "/status", "Status": 200}))

@url.GET("/setup")
def test_get(request):
    data = {}
    data["Command"] = "/test"
    data["Status"] = 200

    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )

    with open("{}/setup.tpl".format(__location__), "r") as f:
        src = Template(f.read())

    return request_response(response=src.substitute())


@url.GET("/devices")
def index_get(request):
    from ..device import get_devices
    data = {}
    try:
        # lights, plugs, blinds, groups, others, batteries = get_sorted_devices(True)

        devices = get_devices(True)
        devices = sorted(devices.items())

        data["Command"] = "/devices"
        data["Status"] = 200
        data["Devices"] = []

        for _, a in devices:
            data["Devices"].append(a.Dictionary)

        data = dumps(data)

        return request_response(response=data, content_type=_content_json)
    except HandshakeError:
        return request_response(status=408)


@url.POST("/setup")
def setup_post(request):
    _config = get_config()
    data = get_post_data(request)
    from ..gateway import create_ident

    print("Post-data: {}".format(data))
    
    try:
        response = create_ident(data["tradfri-ip"], data["tradfri-key"], _config)
        
        if response.get("9091") is not None or response.get("Status") == "ok":
            _config = get_config()
            return request_response(
                response=dumps({"Command": "/setup", "Status": 201}),
                status=201,
                content_type=_content_json,
            )
        else:
            return request_response(
                response=dumps({"Command": "/setup", "Status": 204}),
                status=204,
                content_type=_content_json,
            )

        return request_response(response="Setup ")
    except HandshakeError:
        return request_response(
            response=dumps(
                {"Command": "/setup", "Status": 408, "Error": "HandShake Timeout"}
            ),
            status=408,
            content_type=_content_json,
        )


@url.OPTIONS("/setup")
def setup_options(request):
    print("Option called")
    return request_response(status=200)
