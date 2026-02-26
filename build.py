from dataclasses import dataclass
from enum import auto, IntEnum
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
from typing import Callable, List
import urllib.request
import zipfile

# OS detection
class OS_Type(IntEnum):
    WINDOWS = auto()
    LINUX = auto()

CURR_OS: OS_Type

if sys.platform == "win32":
    CURR_OS = OS_Type.WINDOWS
elif sys.platform == "linux":
    CURR_OS = OS_Type.LINUX
else:
    print("Current OS is not supported.")
    sys.exit(1)

# Download functions
DOWNLOAD_CHUNK_SIZE = 8192
DOWNLOAD_PROGRESS_STEP = 5

class Download_Status(IntEnum):
    SUCCESS = auto()
    FAILURE = auto()

Download_Callback = Callable[[int, int], None]|None

def download_file(url: str, path: str, callback: Download_Callback = None) -> tuple[Download_Status, Exception|None]:
    try:
        request = urllib.request.Request(
            url,
            headers = {
                "User-Agent": "curl/8.18.0"
            }
        )

        with urllib.request.urlopen(request) as response:
            downloaded_size = 0
            total_size_str = response.headers.get("Content-Length")
            total_size = int(total_size_str) if total_size_str else 0

            with open(path, "wb") as file:
                while True:
                    chunk = response.read(DOWNLOAD_CHUNK_SIZE)

                    if not chunk:
                        break

                    file.write(chunk)
                    downloaded_size += len(chunk)

                    if callback:
                        callback(downloaded_size, total_size)

        return Download_Status.SUCCESS, None
    except Exception as e:
        return Download_Status.FAILURE, e

def download_file_and_log(name: str, url: str, path: str) -> None:
    print(f"Downloading {name}...")
    print(f"From: {url}")
    print(f"To: {os.path.abspath(path)}")

    last_step = -1

    def callback(downloaded_size: int, total_size: int) -> None:
        if total_size == 0:
            return

        nonlocal last_step

        percent = int(downloaded_size / total_size * 100)
        current_step = (percent // DOWNLOAD_PROGRESS_STEP) * DOWNLOAD_PROGRESS_STEP

        if current_step > last_step:
            last_step = current_step

            print(f"\rDownload progress: {current_step}%", end = "")

    status, e = download_file(url, path, callback)

    if status == Download_Status.SUCCESS:
        print("\r\033[KDownload success!")
    else:
        print(f"\r\033[KDownload failure: {e}")
        sys.exit(1)

# Unpack functions
class Unpack_Status(IntEnum):
    SUCCESS = auto()
    FAILURE = auto()

def unpack_file(archive_path: str, unpack_path: str, strip_top_level: bool = False) -> tuple[Unpack_Status, Exception|None]:
    archive_path_obj = Path(archive_path)
    unpack_path_obj = Path(unpack_path)

    try:
        if zipfile.is_zipfile(archive_path_obj):
            with zipfile.ZipFile(archive_path_obj, "r") as archive:
                archive.extractall(unpack_path_obj)
        elif tarfile.is_tarfile(archive_path_obj):
            with tarfile.open(archive_path_obj, "r:*") as archive:
                archive.extractall(unpack_path_obj)
        else:
            raise Exception("Unsupported archive type")

        if strip_top_level:
            items = list(unpack_path_obj.iterdir())

            if len(items) == 1 and items[0].is_dir():
                top_folder = items[0]

                for item in top_folder.iterdir():
                    shutil.move(str(item), unpack_path_obj)

                top_folder.rmdir()

        return Unpack_Status.SUCCESS, None
    except Exception as e:
        return Unpack_Status.FAILURE, e

def unpack_file_and_log(name: str, archive_path: str, unpack_path: str, strip_top_level: bool = False) -> None:
    print(f"Unpacking {name}...")

    status, e = unpack_file(archive_path, unpack_path, strip_top_level)

    if status == Unpack_Status.SUCCESS:
        print("Unpacking success!")
    else:
        print(f"Unpacking failure: {e}")
        sys.exit(1)

# Utility
dir_stack = []

def push_dir(path: str) -> None:
    dir_stack.append(os.getcwd())
    os.chdir(path)

def pop_dir() -> None:
    os.chdir(dir_stack.pop())

def merge_files(from_dir: str, to_dir: str) -> None:
    for item in os.listdir(from_dir):
        src_path = os.path.join(from_dir, item)
        dst_path = os.path.join(to_dir, item)

        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, dirs_exist_ok = True)

@dataclass
class Download_Info:
    url: str
    path: str

@dataclass
class Unpack_Info:
    relative_dir: str = ""
    strip_top_level: bool = False

def resolve_download_info(list: dict[OS_Type, Download_Info]) -> None:
    if CURR_OS not in list:
        return None

    return list[CURR_OS]

class Resource_Type(IntEnum):
    CORE = auto()
    EXTENSION = auto()
    PLUGIN = auto()

@dataclass
class Resource:
    type: Resource_Type
    key: str
    name: str
    download_info: Download_Info
    unpack_info: Unpack_Info|None = None

# Config
BUILD_DIR_PATH = "build"

DOWNLOADS_DIR_PATH = os.path.join(BUILD_DIR_PATH, "downloads")
STEAMCMD_DIR_PATH = os.path.join(BUILD_DIR_PATH, "steamcmd")
SERVER_DIR_PATH = os.path.join(BUILD_DIR_PATH, "server")
CSTRIKE_DIR_PATH = os.path.join(SERVER_DIR_PATH, "cstrike")

SOURCEMOD_DIR = os.path.join(CSTRIKE_DIR_PATH, "addons/sourcemod")
SOURCEMOD_SCRIPTING_DIR_PATH = os.path.join(SOURCEMOD_DIR, "scripting")
SOURCEMOD_PLUGINS_DIR_PATH = os.path.join(SOURCEMOD_DIR, "plugins")

RESOURCES_DIR_PATH = os.path.join(BUILD_DIR_PATH, "resources")
RESOURCES_CORE_DIR_PATH = os.path.join(RESOURCES_DIR_PATH, "core")
RESOURCES_EXTENSIONS_DIR_PATH = os.path.join(RESOURCES_DIR_PATH, "extensions")
RESOURCES_PLUGINS_DIR_PATH = os.path.join(RESOURCES_DIR_PATH, "plugins")

CORE_DIR_PATH = "core"
PLUGINS_DIR_PATH = "plugins"

def get_steamcmd_download_info() -> Download_Info:
    if CURR_OS == OS_Type.WINDOWS:
        return Download_Info(
            "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "steamcmd.zip")
        )
    else:
        return Download_Info(
            "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz",
            os.path.join(DOWNLOADS_DIR_PATH, "steamcmd.tar.gz")
        )

def get_steamcmd_executable_path() -> str:
    if CURR_OS == OS_Type.WINDOWS:
        return os.path.join(STEAMCMD_DIR_PATH, "steamcmd.exe")
    else:
        return os.path.join(STEAMCMD_DIR_PATH, "steamcmd.sh")

def get_resource_path(resource: Resource) -> str:
    path = ""

    if resource.type == Resource_Type.CORE:
        path = RESOURCES_CORE_DIR_PATH
    elif resource.type == Resource_Type.EXTENSION:
        path = RESOURCES_EXTENSIONS_DIR_PATH
    else:
        path = RESOURCES_PLUGINS_DIR_PATH

    return os.path.join(path, resource.key)

# Resources
RESOURCES: List[Resource] = []

# Resources | Core
RESOURCES.append(Resource(
    Resource_Type.CORE,
    "sourcemod",
    "SourceMod",
    resolve_download_info({
        OS_Type.WINDOWS: Download_Info(
            "https://sm.alliedmods.net/smdrop/1.12/sourcemod-1.12.0-git7221-windows.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "sourcemod.zip")
        ),
        OS_Type.LINUX: Download_Info(
            "https://sm.alliedmods.net/smdrop/1.12/sourcemod-1.12.0-git7221-linux.tar.gz",
            os.path.join(DOWNLOADS_DIR_PATH, "sourcemod.tar.gz")
        )
    })
))

RESOURCES.append(Resource(
    Resource_Type.CORE,
    "mmsource",
    "Metamod:Source",
    resolve_download_info({
        OS_Type.WINDOWS: Download_Info(
            "https://mms.alliedmods.net/mmsdrop/1.12/mmsource-1.12.0-git1219-windows.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "mmsource.zip")
        ),
        OS_Type.LINUX: Download_Info(
            "https://mms.alliedmods.net/mmsdrop/1.12/mmsource-1.12.0-git1219-linux.tar.gz",
            os.path.join(DOWNLOADS_DIR_PATH, "mmsource.tar.gz")
        )
    })
))

RESOURCES.append(Resource(
    Resource_Type.CORE,
    "tickrate_enabler",
    "Tickrate Enabler",
    resolve_download_info({
        OS_Type.WINDOWS: Download_Info(
            "https://github.com/idk1703/TickrateEnabler/releases/download/v0.5-latest/TickrateEnabler-win-tick100-6e83b42.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "tickrate_enabler.zip")
        ),
        OS_Type.LINUX: Download_Info(
            "https://github.com/idk1703/TickrateEnabler/releases/download/v0.5-latest/TickrateEnabler-linux-tick100-6e83b42.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "tickrate_enabler.zip")
        )
    }),
    Unpack_Info("", True)
))

# Resources | Extensions
RESOURCES.append(Resource(
    Resource_Type.EXTENSION,
    "bzip2",
    "Bzip2 Extension",
    resolve_download_info({
        CURR_OS: Download_Info(
            "https://github.com/epsilonbsp/sm_bzip2/releases/download/v1.0.0/sm_bzip2_v1.0.0.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "bzip2.zip")
        )
    })
))

RESOURCES.append(Resource(
    Resource_Type.EXTENSION,
    "ripext",
    "REST in Pawn Extension",
    resolve_download_info({
        OS_Type.WINDOWS: Download_Info(
            "https://github.com/ErikMinekus/sm-ripext/releases/download/1.3.2/sm-ripext-1.3.2-windows.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "ripext.zip")
        ),
        OS_Type.LINUX: Download_Info(
            "https://github.com/ErikMinekus/sm-ripext/releases/download/1.3.2/sm-ripext-1.3.2-linux.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "ripext.zip")
        )
    })
))

# Resources | Plugins
RESOURCES.append(Resource(
    Resource_Type.PLUGIN,
    "dynamic_channels",
    "Dynamic Channels Plugin",
    resolve_download_info({
        CURR_OS: Download_Info(
            "https://github.com/Vauff/DynamicChannels/archive/refs/heads/master.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "dynamic_channels.zip")
        )
    }),
    Unpack_Info(os.path.join("addons", "sourcemod"), True)
))

# Installation
def init() -> None:
    os.makedirs(DOWNLOADS_DIR_PATH, exist_ok = True)
    os.makedirs(RESOURCES_DIR_PATH, exist_ok = True)

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
    if not os.path.exists(resource.download_info.path):
        download_file_and_log(resource.name, resource.download_info.url, resource.download_info.path)

    path = get_resource_path(resource)
    strip_top_level = False

    if resource.unpack_info:
        path = os.path.join(path, resource.unpack_info.relative_dir)
        strip_top_level = resource.unpack_info.strip_top_level

    if not os.path.isdir(path):
        unpack_file_and_log(resource.name, resource.download_info.path, path, strip_top_level)
    else:
        print(f"{resource.name} is already downloaded.")

    return

def download_resources() -> None:
    for resource in RESOURCES:
        download_resource(resource)

def merge_resource(resource: Resource) -> None:
    path = get_resource_path(resource)

    print(path)

    merge_files(path, CSTRIKE_DIR_PATH)

    return

def merge_resources() -> None:
    for resource in RESOURCES:
        merge_resource(resource)

def merge_overrides() -> None:
    merge_files(CORE_DIR_PATH, CSTRIKE_DIR_PATH)

    for name in os.listdir(PLUGINS_DIR_PATH):
        merge_files(os.path.join(PLUGINS_DIR_PATH, name), CSTRIKE_DIR_PATH)

def build() -> None:
    merge_overrides()

    push_dir(SOURCEMOD_SCRIPTING_DIR_PATH)

    if CURR_OS == OS_Type.WINDOWS:
        subprocess.run(["compile.exe"], input = b"\n")
    else:
        subprocess.run(["compile.sh"], input = b"\n")

    pop_dir()

    merge_files(os.path.join(SOURCEMOD_SCRIPTING_DIR_PATH, "compiled"), SOURCEMOD_PLUGINS_DIR_PATH)

    return

def start_lan() -> None:
    path = ""

    if CURR_OS == OS_Type.WINDOWS:
        path = os.path.join(SERVER_DIR_PATH, "srcds.exe")
    else:
        path = os.path.join(SERVER_DIR_PATH, "srcds_run")

    subprocess.run([
        path,
        "-game", "cstrike",
        "+map", "bhop_ambience",
        "+sv_lan", "1",
        "-maxplayers", "24",
        "-insecure",
        "-log",
        "-console"
    ])

# Commands
argc = len(sys.argv)

if argc < 2:
    print("No arguments specified")
    sys.exit(1)
elif argc > 2:
    print("Too many arguments")
    sys.exit(1)

command = sys.argv[1]

init()

if command == "install_steamcmd":
    install_steamcmd()
elif command == "install_server":
    install_server()
elif command == "download_resources":
    download_resources()
elif command == "merge_resources":
    merge_resources()
elif command == "build":
    build()
elif command == "start_lan":
    start_lan()
else:
    print("No valid command specified")
    sys.exit(1)
