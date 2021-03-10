import os
from ..device import get_sorted_devices, get_devices
from ..errors import HandshakeError, GatewayNotSpecified
from ..config import get_config

from json import dumps
from string import Template

from urllib.parse import parse_qs, parse_qsl

maps = {"GET": {}, "POST": {}}

_config = None
_content_json = "text/json; charset=utf-8"

class request_respons(object):
    _content_type = None
    _response = None
    _status = None

    def __init__(self, status=200, content_type="text/html; charset=utf-8", response=None):
        self._content_type = content_type
        self._status = status
        self._response = response

    @property
    def response(self):
        return self._response.encode("utf-8") if self._response is not None else None

    @response.setter
    def response(self, value):
        self._response = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def content_type(self):
        return self._content_type

class url(object):
    @staticmethod
    def GET(name):
        def wrapper(f):
            maps["GET"][name] = f
            return f

        return wrapper

    @staticmethod
    def POST(name):
        def wrapper(f):
            maps["POST"][name] = f
            return f

        return wrapper


def DumpHTTPResponseToConsole(httpDict):
    if isinstance(httpDict, dict):
        print("HTTP Details (" + str(len(httpDict)) + "):")
        for x in httpDict:
            if isinstance(httpDict[x], dict):
                print("--->'" + x + " (" + str(len(httpDict[x])) + "):")
                for y in httpDict[x]:
                    print("------->'" + y + "':'" + str(httpDict[x][y]) + "'")
            else:
                print("--->'" + x + "':'" + str(httpDict[x]) + "'")

def get_post_data(request):
    return dict(parse_qsl(request["Data"].decode('utf-8')))

@url.GET("/devices")
def index_get(request):
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

        return request_respons(response=data, content_type=_content_json)
    except HandshakeError:
        return request_respons(status=408)

@url.GET("/setup")
def test_get(request):
    data = {}
    data["Command"] = "/test"
    data["Status"] = 200

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open("{}/setup.tpl".format(__location__), "r") as f:
        src = Template(f.read())
 
    return request_respons(response=src.substitute())

@url.POST("/setup")
def setup_post(request):
    data = get_post_data(request)
    from ..gateway import create_ident
    try:
        response = create_ident(data['tradfri-ip'], data['tradfri-key'], _config)
        
        print(response)

        if response.get("9091") is not None or response.get("Status") == "ok":
            return request_respons(response=dumps({'Command': '/setup', 'Status': 201}), status=201, content_type=_content_json)
        else:
            return request_respons(response=dumps({'Command': '/setup', 'Status': 204}), status=204, content_type=_content_json)

        return request_respons(response="Setup ")
    except HandshakeError:
        return request_respons(response=dumps({'Command': '/setup', 'Status': 408, 'Error': 'HandShake Timeout'}), status=408, content_type=_content_json)

def handle_request(Data=None):
    # DumpHTTPResponseToConsole(Data)
    
    global _config

    _config = get_config()

    verb = Data.get("Verb")
    url = Data.get("URL")

    try:
        if verb is not None:
            if maps[verb].get(url) is not None:
                return maps[verb][url](Data)
            else:
                print("Not found")
                return request_respons(status=404, response=dumps({"Command": url, "Status": 404}))
        else:
            print("Unknown verb {}".format(verb))
    except GatewayNotSpecified:
        return request_respons(status=701, response=dumps({"Command": url, "Status": 701, "Error": "Gateway config not set"}))

    return None
