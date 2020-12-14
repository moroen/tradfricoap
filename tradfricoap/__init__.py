__version__ = "0.0.15"


class Error(Exception):
    pass


class IllegalMethodError(Exception):
    pass


class ApiNotFoundError(Error):
    def __init__(self, api, message):
        self.message = message
        self.api = api
