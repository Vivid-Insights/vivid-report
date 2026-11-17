"""Small local web server: chat page, help page, JSON chat endpoint."""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import llm
from .content import load
from .engine import Engine

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
PAGES = {"/": "index.html", "/index.html": "index.html", "/help": "help.html", "/help.html": "help.html"}
MAX_BODY = 16_384


def make_handler(engine: Engine):
    class Handler(BaseHTTPRequestHandler):
        server_version = "AskAshbourne/1"

        def log_message(self, fmt, *args):  # no message content in logs (data minimisation)
            pass

        def _send(self, code: int, body: bytes, ctype: str):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, code: int, obj):
            self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

        def do_GET(self):
            path = self.path.split("?", 1)[0]
            if path in PAGES:
                with open(os.path.join(STATIC_DIR, PAGES[path]), "rb") as fh:
                    self._send(200, fh.read(), "text/html; charset=utf-8")
            elif path == "/api/config":
                bot = load().bot
                self._json(200, {"title": bot["projectTitle"], "disclaimer": bot["disclaimer"],
                                 "mode": "live" if llm.live_mode() else "offline"})
            elif path == "/health":
                self._json(200, {"ok": True})
            else:
                self._json(404, {"error": "not found"})

        def do_POST(self):
            path = self.path.split("?", 1)[0]
            length = int(self.headers.get("Content-Length") or 0)
            if length > MAX_BODY:
                return self._json(413, {"error": "message too long"})
            try:
                data = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
            except (ValueError, UnicodeDecodeError):
                return self._json(400, {"error": "invalid JSON"})
            if path == "/api/chat":
                msg = data.get("message")
                if not isinstance(msg, str) or not msg.strip():
                    return self._json(400, {"error": "message is required"})
                out = engine.handle(data.get("session_id"), msg, data.get("facet_id"))
                return self._json(200, out)
            if path == "/api/reset":
                engine.reset(data.get("session_id"))
                return self._json(200, {"ok": True})
            return self._json(404, {"error": "not found"})

    return Handler


def make_server(host: str = "127.0.0.1", port: int = 8000, engine: Engine | None = None) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), make_handler(engine or Engine()))
