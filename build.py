# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 EpsilonBSP

import os
import sys

sys.pycache_prefix = os.path.join("build", "pycache")

from source.install import *
from source.os_type import *

OS_TYPE = get_os_type()

if OS_TYPE == 0:
    print("Current OS is not supported.")
    sys.exit(1)

argc = len(sys.argv)

if argc < 2:
    print("No arguments specified")
    sys.exit(1)
elif argc > 3:
    print("Too many arguments")
    sys.exit(1)

command = sys.argv[1]
arg0 = sys.argv[2] if argc > 2 else ""

if command == "install_steamcmd":
    install_steamcmd()
elif command == "install_server":
    install_server()
elif command == "download_all_resources":
    download_all_resources()
elif command == "download_resource":
    if not arg0:
        print("ERROR: Resource key not specified.")
        sys.exit(1)

    download_one_resource(arg0)
elif command == "merge_resources":
    merge_all_resources()
elif command == "merge_resource":
    if not arg0:
        print("ERROR: Resource key not specified.")
        sys.exit(1)

    merge_one_resource(arg0)
elif command == "compile_all_resources":
    compile_all_resources()
elif command == "compile_resource":
    if not arg0:
        print("ERROR: Resource key not specified.")
        sys.exit(1)

    compile_one_resource(arg0)
elif command == "install_all":
    install_steamcmd()
    install_server()
    download_all_resources()
    merge_all_resources()
    compile_all_resources()
elif command == "start_lan":
    start_lan()
elif command == "start_fastdl":
    start_fastdl()
else:
    print("No valid command specified")
    sys.exit(1)
