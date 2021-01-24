from ..device import get_sorted_devices
from ..errors import HandshakeError

from json import dumps

maps = {"GET": {}, "POST": {}}

class request_respons(object):
    _headers = {}
    _response = None
    _status = None

    def __init__(self, status=200, headers=None, response=None):
        self._headers = {"Connection": "keep-alive", "Content-Type": "text/html; charset=utf-8"}
        self._status = status
        self._headers = headers
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
    def headers(self):
        return self._headers

class url(object):
    @staticmethod
    def GET(name):
        def wrapper(f):
            maps["GET"][name] = f
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


@url.GET("/devices")
def index_get():
    data = {}
    try:
        lights, plugs, blinds, groups, others, batteries = get_sorted_devices(True)
        data["Command"] = "/devices"
        data["Status"] = 200
        data["Devices"] = {}

        data["Devices"]["Lights"] = []
        data["Devices"]["Plugs"] = []
        data["Devices"]["Blinds"] = []
        data["Devices"]["Groups"] = []
        data["Devices"]["Batteries"] = []
        data["Devices"]["Others"] = []

        for a in lights:
            data["Devices"]["Lights"].append(a.Dictionary)

        for a in plugs:
            data["Devices"]["Plugs"].append(a.Dictionary)

        for a in blinds:
            data["Devices"]["Blinds"].append(a.Dictionary)

        for a in groups:
            data["Devices"]["Groups"].append(a.Dictionary)

        for a in batteries:
            data["Devices"]["Batteries"].append(a.Dictionary)

        for a in others:
            data["Devices"]["Others"].append(a.Dictionary)

        data = dumps(data)     

        return request_respons(response=data)
    except HandshakeError:
        return request_respons(status=408)
        

def handle_request(Data):
    DumpHTTPResponseToConsole(Data)

    verb = Data.get("Verb")
    url = Data.get("URL")

    if verb is not None:
        if maps[verb].get(url) is not None:
            return maps[verb][url]()
        else:
            print("Not found")
            return request_respons(status=404, response=dumps({"Command": url, "Status": 404}))
    else:
        print("Unknown verb {}".format(verb))

    return None
