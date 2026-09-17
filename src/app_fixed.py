#!/usr/bin/env python3
"""Remediated local demo app for defensive assessment training."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import secrets
import urllib.parse

logging.basicConfig(level=logging.INFO, format="%(asctime)s security_event=%s")
USERS = {"student": "Password123!"}
MAX_NAME_LEN = 80

def valid_name(name):
    return (
        isinstance(name, str)
        and 1 <= len(name) <= MAX_NAME_LEN
        and all(ch.isalnum() or ch in " ._-'" for ch in name)
    )

class Handler(BaseHTTPRequestHandler):
    def send_json(self, code, data, headers=None):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
        self.send_header("Cache-Control", "no-store")
        if headers:
            for k, v in headers.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path == "/login":
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(min(length, 4096)).decode(errors="replace")
            data = urllib.parse.parse_qs(raw)
            username = data.get("username", [""])[0]
            password = data.get("password", [""])[0]

            # Never log passwords or tokens.
            logging.info("login_attempt username=%s result=%s",
                         username[:64], "success" if USERS.get(username) == password else "failure")

            if USERS.get(username) == password:
                token = secrets.token_urlsafe(32)
                self.send_json(200, {"status": "ok"}, {"Set-Cookie": f"session={token}; HttpOnly; SameSite=Strict"})
            else:
                self.send_json(401, {"status": "error"})

        elif self.path == "/profile":
            length = int(self.headers.get("Content-Length", "0"))
            if length > 2048:
                self.send_json(413, {"status": "error", "message": "payload too large"})
                return
            try:
                data = json.loads(self.rfile.read(length).decode() or "{}")
            except (ValueError, UnicodeDecodeError):
                self.send_json(400, {"status": "error", "message": "invalid JSON"})
                return

            name = data.get("name", "")
            if not valid_name(name):
                self.send_json(400, {"status": "error", "message": "invalid name"})
                return
            self.send_json(200, {"status": "ok", "name": name})
        else:
            self.send_json(404, {"status": "error"})

if __name__ == "__main__":
    print("SECURED TRAINING APP: localhost only")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
