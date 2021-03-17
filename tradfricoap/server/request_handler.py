import os

from importlib import reload
from json import dumps

from ..device import get_sorted_devices, get_devices
from ..errors import HandshakeError, GatewayNotSpecified
from .routes import routes
from .request_response import request_response

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


def handle_request(Data=None):
    # DumpHTTPResponseToConsole(Data)

    verb = Data.get("Verb")
    url = Data.get("URL")

    # print("{}: {}".format(verb, url))

    try:
        if verb is not None:
            if routes[verb].get(url) is not None:
                return routes[verb][url](Data)
            else:
                print("Not found")
                return request_response(
                    status=404, response=dumps({"Command": url, "Status": 404})
                )
        else:
            print("Unknown verb {}".format(verb))
    except GatewayNotSpecified:
        return request_response(
            status=471,
            response=dumps(
                {"Command": url, "Status": 471, "Error": "Gateway config not set"}
            ),
        )

    return None
