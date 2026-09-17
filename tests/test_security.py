import io
import json
import logging
import unittest
from unittest.mock import patch

from src.app_fixed import Handler, valid_name

class DummyRequest:
    def __init__(self, body=b"", headers=None, path="/profile"):
        self.body = io.BytesIO(body)
        self.headers = headers or {}
        self.path = path
        self.wfile = io.BytesIO()
        self.response = None
        self.headers_sent = []

    def send_response(self, code): self.response = code
    def send_header(self, k, v): self.headers_sent.append((k, v))
    def end_headers(self): pass
    def log_request(self, *args): pass
    def rfile_read(self, n): return self.body.read(n)

class SecurityTests(unittest.TestCase):
    def test_name_validation(self):
        self.assertTrue(valid_name("Alice Smith"))
        self.assertFalse(valid_name("<script>alert(1)</script>"))
        self.assertFalse(valid_name("A" * 81))

    def test_login_does_not_log_password(self):
        class TestHandler(Handler):
            def __init__(self):
                self.rfile = io.BytesIO(b"username=student&password=TEST_PASSWORD")
                self.headers = {"Content-Length": "40"}
                self.path = "/login"
                self.wfile = io.BytesIO()
                self.sent = []
            def send_response(self, code): self.sent.append(("status", code))
            def send_header(self, k, v): self.sent.append((k, v))
            def end_headers(self): pass

        h = TestHandler()
        with self.assertLogs(level="INFO") as cm:
            h.do_POST()
        joined = "\n".join(cm.output)
        self.assertNotIn("TEST_PASSWORD", joined)
        self.assertIn("login_attempt", joined)

if __name__ == "__main__":
    unittest.main()
