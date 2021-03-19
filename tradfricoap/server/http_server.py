from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from importlib import reload

import tradfricoap.server.request_handler as server
import json
from urllib.parse import parse_qs, parse_qsl


class request_handler(BaseHTTPRequestHandler):
    Data = {}

    def _set_response(self, response_code, content_type):
        self.send_response(response_code)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        logging.info(
            "GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers)
        )

        Data = {"Verb": "GET", "URL": self.path}

        reload(server)
        page = server.handle_request(Data)
        self._set_response(page.status, page.content_type)

        if page.response is not None:
            self.wfile.write(page.response)
        else:
            self.wfile.write("".encode("utf-8"))

    def do_POST(self):
        logging.info(
            "POST request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers)
        )

        content_length = int(
            self.headers["Content-Length"]
        )  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself

        Data = {"Verb": "POST", "URL": self.path, "Data": post_data}

        reload(server)
        page = server.handle_request(Data)
        self._set_response(page.status, page.content_type)

        if page.response is not None:
            self.wfile.write(page.response)
        else:
            self.wfile.write("".encode("utf-8"))


def run_server(server_class=HTTPServer, handler_class=request_handler, port=8085):
    logging.basicConfig(level=logging.INFO)
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")
