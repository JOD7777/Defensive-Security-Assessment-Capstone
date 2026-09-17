#!/usr/bin/env python3
"""Intentionally insecure local demo app for defensive assessment training.

DO NOT expose this service to a network. It is designed for localhost-only testing.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import urllib.parse

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
USERS = {"student": "Password123!"}

class Handler(BaseHTTPRequestHandler):
    def send_json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path == "/login":
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode()
            data = urllib.parse.parse_qs(raw)
            username = data.get("username", [""])[0]
            password = data.get("password", [""])[0]

            # Finding: password is written to logs.
            logging.info("login username=%s password=%s", username, password)

            if USERS.get(username) == password:
                # Finding: predictable/static session value.
                self.send_json(200, {"status": "ok", "session": "SESSION123"})
            else:
                self.send_json(401, {"status": "error"})

        elif self.path == "/profile":
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length).decode() or "{}")
            name = data.get("name", "")

            # Finding: no length/character validation.
            self.send_json(200, {"status": "ok", "name": name})
        else:
            self.send_json(404, {"status": "error"})

if __name__ == "__main__":
    print("INSECURE TRAINING APP: localhost only")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
