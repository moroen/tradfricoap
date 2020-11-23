import logging
import subprocess
import os
import json
from shutil import which

from .config import get_config
from . import ApiNotFoundError


class HandshakeError(Exception):
    pass


class UriNotFoundError(Exception):
    pass


class ReadTimeoutError(Exception):
    pass


class WriteTimeoutError(Exception):
    pass


class MethodNotAllowedError(Exception):
    pass


_coapCMD = "coapcmd"


def close_connection():
    pass


def set_debug_level(level):
    pass


def set_coapcmd(cmd):
    global _coapCMD
    _coapCMD = cmd


def raise_error(result):
    if result["Status"] == "HandshakeError":
        raise HandshakeError
    if result["Status"] == "UriNotFound":
        raise UriNotFoundError
    if result["Status"] == "ReadTimeoutError":
        raise ReadTimeoutError
    if result["Status"] == "WriteTimeoutError":
        raise WriteTimeoutError
    if result["Status"] == "MethodNotAllowed":
        raise MethodNotAllowedError
    return None


def request(uri, payload=None, method="put"):
    if which(_coapCMD) is None:
        raise ApiNotFoundError(
            "coapcmd", "'coapcmd' not found! Looking for {}".format(_coapCMD)
        )

    conf = get_config().configuation
    path = "coaps://{}:{}/{}".format(conf["Gateway"], 5684, uri)

    if conf["Gateway"] is None:
        logging.critical("Gateway not specified")
        return

    if payload is None:
        try:
            result = subprocess.run(
                [
                    _coapCMD,
                    "get",
                    "--ident",
                    conf["Identity"],
                    "--key",
                    conf["Passkey"],
                    path,
                ],
                stdout=subprocess.PIPE,
            ).stdout.decode("utf-8")

            result = json.loads(result)

            if result["Status"] == "ok":
                return result["Result"]
            else:
                raise_error(result)
            return None

        except json.JSONDecodeError:
            print("Unexpected result from gateway in coapcmd_get: {}".format(result))

    else:
        try:
            result = subprocess.run(
                [
                    _coapCMD,
                    method,
                    "--ident",
                    conf["Identity"],
                    "--key",
                    conf["Passkey"],
                    path,
                    payload,
                ],
                stdout=subprocess.PIPE,
            ).stdout.decode("utf-8")

            result = json.loads(result)
            if result["Status"] == "ok":
                return result["Result"]
            else:
                raise_error(result)
        except json.JSONDecodeError:
            print("Unexpected result from gateway in coapcmd_put: {}".format(result))


def get_version():
    try:
        coapcmd_version = "({}) {}".format(
            _coapCMD,
            subprocess.run(
                [
                    _coapCMD,
                    "version",
                ],
                stdout=subprocess.PIPE,
            ).stdout.decode("utf-8"),
        )
    except FileNotFoundError:
        coapcmd_version = "Not found (Looking for {}).\n".format(_coapCMD)

    return coapcmd_version


def create_ident(ip, key, conf_obj):
    import uuid
    from .config import host_config, get_config
    from json import loads, dumps

    identity = uuid.uuid4().hex

    payload = '{{"{}":"{}"}}'.format(9090, identity)
    uri = "coaps://{}:{}/{}".format(ip, 5684, "15011/9063")

    result = json.loads(
        subprocess.run(
            [
                _coapCMD,
                "post",
                "--ident",
                "Client_identity",
                "--key",
                key,
                uri,
                payload,
            ],
            stdout=subprocess.PIPE,
        ).stdout.decode("utf-8")
    )
    logging.debug("Create ident result: {}".format(result))

    print(result)

    if result is None:
        logging.critical("Create_ident: No data from gateway")
        return None

    if result["Status"] == "ok":
        res = json.loads(result["Result"])
        conf_obj.set_config_items(Gateway=ip, Identity=identity, Passkey=res["9091"])
        conf_obj.save()

    if result["Status"] == "HandshakeError":
        raise HandshakeError
    if result["Status"] == "UriNotFound":
        raise UriNotFoundError
    if result["Status"] == "ReadTimeoutError":
        raise ReadTimeoutError
    if result["Status"] == "WriteTimeoutError":
        raise WriteTimeoutError
    return None
