# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 EpsilonBSP

import http.server
import os
import subprocess
import sys

from .config import *
from .download import *
from .file_system import *
from .unpack import *

def start_lan() -> None:
    if not os.path.isdir(SERVER_DIR_PATH):
        print("Server is not installed.")
        sys.exit(1)

    subprocess.run([
        get_srcds_path(),
        "-game", "cstrike",
        "+map", "bhop_ambience",
        "+sv_lan", "1",
        "-maxplayers", "24",
        "-insecure",
        "-log",
        "-console"
    ])

class FastDLHandler(http.server.SimpleHTTPRequestHandler):
    def _allowed(self) -> bool:
        parts = self.path.lstrip("/").split("/")

        return parts[0] in FASTDL_DIRS

    def do_GET(self):
        if not self._allowed():
            self.send_error(403)

            return

        super().do_GET()

    def do_HEAD(self):
        if not self._allowed():
            self.send_error(403)

            return

        super().do_HEAD()

def start_fastdl() -> None:
    if not os.path.isdir(CSTRIKE_DIR_PATH):
        print("Server is not installed.")
        sys.exit(1)

    os.chdir(CSTRIKE_DIR_PATH)

    port = 8080

    with http.server.HTTPServer(("", port), FastDLHandler) as httpd:
        print(f"FastDL serving {CSTRIKE_DIR_PATH} on port {port}")
        httpd.serve_forever()
