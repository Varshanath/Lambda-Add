import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from lambda_function import lambda_handler

PORT = 8000


class Handler(BaseHTTPRequestHandler):
    def _handle(self, body=None):
        parsed = urlparse(self.path)
        query = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        event = {"queryStringParameters": query, "body": body}

        response = lambda_handler(event, None)

        self.send_response(response["statusCode"])
        for key, value in response.get("headers", {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response["body"].encode("utf-8"))

    def do_GET(self):
        self._handle()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length).decode("utf-8") if length else None
        self._handle(body=raw_body)

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), Handler)
    print(f"Serving lambda_handler on http://localhost:{PORT}")
    print(f"Try: curl 'http://localhost:{PORT}/?a=2&b=3'")
    server.serve_forever()
