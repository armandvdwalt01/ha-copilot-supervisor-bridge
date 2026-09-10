#!/usr/bin/env python3
"""Minimal, token-protected Supervisor bridge with explicit operation gates."""

from __future__ import annotations

import json
import os
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


TOKEN = os.environ["BRIDGE_ACCESS_TOKEN"]
SUPERVISOR_TOKEN = os.environ["SUPERVISOR_TOKEN"]
SUPERVISOR = "http://supervisor"
FLAGS = {
    "restart_core": os.environ["ALLOW_CORE_RESTART"] == "true",
    "app_management": os.environ["ALLOW_APP_MANAGEMENT"] == "true",
    "backup_restore": os.environ["ALLOW_BACKUP_RESTORE"] == "true",
    "log_read": os.environ["ALLOW_LOG_READ"] == "true",
    "hacs_management": os.environ["ALLOW_HACS_MANAGEMENT"] == "true",
}


def supervisor(path: str, method: str = "GET", body: bytes | None = None) -> tuple[int, str]:
    command = [
        "curl",
        "-sS",
        "-X",
        method,
        "-H",
        f"Authorization: Bearer {SUPERVISOR_TOKEN}",
    ]
    if body is not None:
        command.extend(["-H", "Content-Type: application/json", "--data-binary", "@-"])
    command.append(f"{SUPERVISOR}{path}")
    result = subprocess.run(command, input=body, capture_output=True, check=False)
    return result.returncode, result.stdout.decode(errors="replace")


class Handler(BaseHTTPRequestHandler):
    def _authorized(self) -> bool:
        return self.headers.get("Authorization") == f"Bearer {TOKEN}"

    def _json(self, status: int, payload: object) -> None:
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if not self._authorized():
            self._json(401, {"error": "unauthorized"})
            return
        if self.path == "/health":
            self._json(200, {"ok": True, "operations": FLAGS})
            return
        if self.path == "/apps":
            if not FLAGS["app_management"]:
                self._json(403, {"error": "app management disabled"})
                return
            _, output = supervisor("/addons")
            self._json(200, {"raw": output})
            return
        if self.path == "/logs":
            if not FLAGS["log_read"]:
                self._json(403, {"error": "log access disabled"})
                return
            _, output = supervisor("/core/logs")
            self._json(200, {"raw": output})
            return
        self._json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if not self._authorized():
            self._json(401, {"error": "unauthorized"})
            return
        if self.path == "/core/restart":
            if not FLAGS["restart_core"]:
                self._json(403, {"error": "core restart disabled"})
                return
            code, output = supervisor("/core/restart", "POST")
            self._json(200 if code == 0 else 502, {"result": output})
            return
        self._json(404, {"error": "not found"})

    def log_message(self, *_args: object) -> None:
        return


ThreadingHTTPServer(("0.0.0.0", 8126), Handler).serve_forever()
