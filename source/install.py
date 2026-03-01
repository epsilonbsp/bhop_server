# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 EpsilonBSP

import os
import shutil
import subprocess
import sys
import time

from .config import *
from .download import *
from .file_system import *
from .unpack import *

def install_steamcmd(reinstall = False) -> None:
    if os.path.isdir(STEAMCMD_DIR_PATH):
        if reinstall:
            shutil.rmtree(STEAMCMD_DIR_PATH)
        else:
            print("SteamCMD is already installed.")

            return

    download_info = get_steamcmd_download_info()

    download_file_and_log("SteamCMD", download_info.url, download_info.path)
    unpack_file_and_log("SteamCMD", download_info.path, STEAMCMD_DIR_PATH)

    print("Installing SteamCMD...")

    subprocess.run([
        get_steamcmd_executable_path(),
        "+login",
        "anonymous",
        "+logout",
        "+quit"
    ])

    print("SteamCMD is successfully installed!")

def install_server(reinstall = False):
    if not os.path.isdir(STEAMCMD_DIR_PATH):
        print("SteamCMD is not installed.")
        sys.exit(1)

    if os.path.isdir(SERVER_DIR_PATH):
        if reinstall:
            shutil.rmtree(SERVER_DIR_PATH)
        else:
            print("Server is already installed.")

            return

    print("Installing Counter Strike: Source Dedicated Server...")

    subprocess.run([
        get_steamcmd_executable_path(),
        "+force_install_dir", os.path.abspath(SERVER_DIR_PATH),
        "+login", "anonymous",
        "+app_update", "232330", "validate",
        "+logout",
        "+quit"
    ])

    print("Counter Strike: Source Dedicated Server is successfully installed!")

def download_resource(resource: Resource) -> None:
    if not resource.download_info:
        return

    if not os.path.exists(resource.download_info.path):
        download_file_and_log(resource.name, resource.download_info.url, resource.download_info.path)
    else:
        print(f"{resource.name} is already downloaded.")

    path = resource.install_dir
    strip_top_level = False

    if resource.unpack_info:
        path = os.path.join(resource.install_dir, resource.unpack_info.wrapper_path)
        strip_top_level = resource.unpack_info.strip_top_level

    if not os.path.isdir(resource.install_dir):
        unpack_file_and_log(resource.name, resource.download_info.path, path, strip_top_level)
    else:
        print(f"{resource.name} is already unpacked.")

def download_resources() -> None:
    for resource in RESOURCES.values():
        download_resource(resource)

        time.sleep(0.5)

def compile_resource(resource: Resource) -> None:
    if len(resource.plugin_paths) == 0:
        return

    default_include_dir_path = os.path.join(resource.install_dir, REL_SM_SCRIPTING_DIR_PATH, "include")

    for plugin_path in resource.plugin_paths:
        input_path = os.path.join(resource.install_dir, plugin_path)
        output_path = os.path.join(COMPILED_DIR_PATH, os.path.basename(plugin_path).rsplit(".sp", 1)[0] + ".smx")
        include_paths = ["-i", default_include_dir_path]

        if len(resource.include_paths) > 0:
            for include_path in resource.include_paths:
                include_paths.append("-i")
                include_paths.append(include_path)

        print(f"Compiling {resource.name}...")

        subprocess.run([get_sourcemod_spcomp_path(), *include_paths, "-o", output_path, input_path])

def merge_resource(resource: Resource) -> None:
    if len(resource.merge_paths) == 0:
        print(f"No merge paths specified for {resource.name}.")

        return

    print(f"Merging {resource.name}...")

    for merge_path in resource.merge_paths:
        from_path = os.path.join(resource.install_dir, merge_path)
        to_path = os.path.join(CSTRIKE_DIR_PATH, merge_path)

        print(f"Merging from {from_path} to {to_path}")

        os.makedirs(to_path, exist_ok = True)
        merge_files(from_path, to_path)

def merge_resources(key: str = "") -> None:
    if not os.path.isdir(SERVER_DIR_PATH):
        print("Server is not installed.")
        sys.exit(1)

    for resource in RESOURCES.values():
        if key and resource.key != key:
            continue

        merge_resource(resource)

    print(f"Merging {CORE_DIR_PATH} into {CSTRIKE_DIR_PATH}.")
    merge_files(CORE_DIR_PATH, CSTRIKE_DIR_PATH)

def compile_resources(key: str = "") -> None:
    os.makedirs(COMPILED_DIR_PATH, exist_ok = True)

    for resource in RESOURCES.values():
        if key and resource.key != key:
            continue

        compile_resource(resource)

    os.makedirs(SOURCEMOD_PLUGINS_DIR_PATH, exist_ok = True)

    print(f"Clearing {SOURCEMOD_PLUGINS_DIR_PATH}.")
    clear_dir(SOURCEMOD_PLUGINS_DIR_PATH)

    print(f"Merging {COMPILED_DIR_PATH} into {SOURCEMOD_PLUGINS_DIR_PATH}.")
    merge_files(COMPILED_DIR_PATH, SOURCEMOD_PLUGINS_DIR_PATH)

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
