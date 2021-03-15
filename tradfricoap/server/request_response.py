_content_json = "text/json; charset=utf-8"

class request_response(object):
    _content_type = None
    _response = None
    _status = None

    def __init__(
        self, status=200, content_type="text/html; charset=utf-8", response=None
    ):
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
