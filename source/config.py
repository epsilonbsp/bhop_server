# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 EpsilonBSP

import os

from .os_type import *
from .resource import *

# General
BUILD_DIR_PATH = "build"
COMPILED_DIR_PATH = os.path.join(BUILD_DIR_PATH, "compiled")
DOWNLOADS_DIR_PATH = os.path.join(BUILD_DIR_PATH, "downloads")
SCRIPTING_DIR_PATH = os.path.join("addons", "sourcemod", "scripting")

# SteamCMD
STEAMCMD_DIR_PATH = os.path.join(BUILD_DIR_PATH, "steamcmd")

def get_steamcmd_download_info() -> Download_Info:
    if get_os_type() == OS_Type.WINDOWS:
        return Download_Info(
            "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "steamcmd.zip")
        )

    return Download_Info(
        "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz",
        os.path.join(DOWNLOADS_DIR_PATH, "steamcmd.tar.gz")
    )

def get_steamcmd_executable_path() -> str:
    if get_os_type() == OS_Type.WINDOWS:
        return os.path.join(STEAMCMD_DIR_PATH, "steamcmd.exe")

    return os.path.join(STEAMCMD_DIR_PATH, "steamcmd.sh")

# Server
SERVER_DIR_PATH = os.path.join(BUILD_DIR_PATH, "server")
CSTRIKE_DIR_PATH = os.path.join(SERVER_DIR_PATH, "cstrike")
ADDONS_DIR_PATH = os.path.join(CSTRIKE_DIR_PATH, "addons")
SOURCEMOD_DIR_PATH = os.path.join(ADDONS_DIR_PATH, "sourcemod")
SOURCEMOD_SCRIPTING_DIR_PATH = os.path.join(SOURCEMOD_DIR_PATH, "scripting")
SOURCEMOD_PLUGINS_DIR_PATH = os.path.join(SOURCEMOD_DIR_PATH, "plugins")

def get_srcds_path() -> str:
    if get_os_type() == OS_Type.WINDOWS:
        return os.path.join(SERVER_DIR_PATH, "srcds.exe")

    return os.path.join(SERVER_DIR_PATH, "srcds_run")

# Resources
RESOURCES_DIR_PATH = os.path.join(BUILD_DIR_PATH, "resources")
RESOURCES_CORE_DIR_PATH = os.path.join(RESOURCES_DIR_PATH, "core")
RESOURCES_EXTENSIONS_DIR_PATH = os.path.join(RESOURCES_DIR_PATH, "extensions")
RESOURCES_PLUGINS_DIR_PATH = os.path.join(RESOURCES_DIR_PATH, "plugins")

CORE_DIR_PATH = "core"
EXTENSIONS_DIR_PATH = "plugins"
PLUGINS_DIR_PATH = "plugins"

class Resource_Key(IntEnum):
    SOURCEMOD = 0
    METAMOD_SOURCE = auto()
    TICKRATE_ENABLER = auto()
    BZIP2 = auto()
    EVENTQUEUEFIXFIX = auto()
    RIPEXT = auto()
    DYNAMIC_CHANNELS = auto()
    BHOPTIMER = auto()
    JUMPSTATS = auto()
    LANDFIX = auto()
    MAPLOADER = auto()
    PUSH_FIX_DE = auto()
    RNGFIX = auto()
    SHOW_PLAYER_CLIPS = auto()
    SHOWTRIGGERS = auto()

RESOURCES: dict[int, Resource] = {}

RESOURCES[Resource_Key.SOURCEMOD] = Resource(
    type = Resource_Type.CORE,
    key = "sourcemod",
    name = "SourceMod",
    install_dir = os.path.join(RESOURCES_CORE_DIR_PATH, "sourcemod"),
    merge_paths = [],
    plugin_paths = [
        os.path.join(SCRIPTING_DIR_PATH, "admin-flatfile.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "adminhelp.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "adminmenu.sp"),
        # os.path.join(SCRIPTING_DIR_PATH, "admin-sql-prefetch.sp"),
        # os.path.join(SCRIPTING_DIR_PATH, "admin-sql-threaded.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "antiflood.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "basebans.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "basechat.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "basecomm.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "basecommands.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "basetriggers.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "basevotes.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "clientprefs.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "funcommands.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "funvotes.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "mapchooser.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "nextmap.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "nominations.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "playercommands.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "randomcycle.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "reservedslots.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "rockthevote.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "sounds.sp"),
        # os.path.join(SCRIPTING_DIR_PATH, "sql-admin-manager.sp")
    ],
    download_info = resolve_download_info({
        OS_Type.WINDOWS: Download_Info(
            "https://sm.alliedmods.net/smdrop/1.12/sourcemod-1.12.0-git7221-windows.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "sourcemod.zip")
        ),
        OS_Type.LINUX: Download_Info(
            "https://sm.alliedmods.net/smdrop/1.12/sourcemod-1.12.0-git7221-linux.tar.gz",
            os.path.join(DOWNLOADS_DIR_PATH, "sourcemod.tar.gz")
        )
    }),
    unpack_info = None
)

RESOURCES[Resource_Key.METAMOD_SOURCE] = Resource(
    type = Resource_Type.CORE,
    key = "metamod_source",
    name = "Metamod:Source",
    install_dir = os.path.join(RESOURCES_CORE_DIR_PATH, "metamod_source"),
    merge_paths = [],
    plugin_paths = [],
    download_info = resolve_download_info({
        OS_Type.WINDOWS: Download_Info(
            "https://mms.alliedmods.net/mmsdrop/1.12/mmsource-1.12.0-git1219-windows.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "metamod_source.zip")
        ),
        OS_Type.LINUX: Download_Info(
            "https://mms.alliedmods.net/mmsdrop/1.12/mmsource-1.12.0-git1219-linux.tar.gz",
            os.path.join(DOWNLOADS_DIR_PATH, "metamod_source.tar.gz")
        )
    }),
    unpack_info = None
)

RESOURCES[Resource_Key.TICKRATE_ENABLER] = Resource(
    type = Resource_Type.CORE,
    key = "tickrate_enabler",
    name = "Tickrate Enabler",
    install_dir = os.path.join(RESOURCES_CORE_DIR_PATH, "tickrate_enabler"),
    merge_paths = [],
    plugin_paths = [],
    download_info = resolve_download_info({
        OS_Type.WINDOWS: Download_Info(
            "https://github.com/idk1703/TickrateEnabler/releases/download/v0.5-latest/TickrateEnabler-win-tick100-6e83b42.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "tickrate_enabler.zip")
        ),
        OS_Type.LINUX: Download_Info(
            "https://github.com/idk1703/TickrateEnabler/releases/download/v0.5-latest/TickrateEnabler-linux-tick100-6e83b42.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "tickrate_enabler.zip")
        )
    }),
    unpack_info = Unpack_Info("", True)
)

RESOURCES[Resource_Key.BZIP2] = Resource(
    type = Resource_Type.EXTENSION,
    key = "bzip2",
    name = "Bzip2 Extension",
    install_dir = os.path.join(RESOURCES_EXTENSIONS_DIR_PATH, "bzip2"),
    merge_paths = [],
    plugin_paths = [],
    download_info = resolve_download_info({
        get_os_type(): Download_Info(
            "https://github.com/epsilonbsp/sm_bzip2/releases/download/v1.0.0/sm_bzip2_v1.0.0.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "bzip2.zip")
        )
    }),
    unpack_info = None
)

RESOURCES[Resource_Key.EVENTQUEUEFIXFIX] = Resource(
    type = Resource_Type.EXTENSION,
    key = "eventqueuefixfix",
    name = "Event Queue Fix Fix",
    install_dir = os.path.join(RESOURCES_EXTENSIONS_DIR_PATH, "eventqueuefixfix"),
    merge_paths = [],
    plugin_paths = [],
    download_info = resolve_download_info({
        OS_Type.WINDOWS: Download_Info(
            "https://github.com/srcwr/eventqueuefixfix/releases/download/v1.0.1/eventqueuefixfix-v1.0.1-def5b0e-windows-x32.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "eventqueuefixfix.zip")
        )
    }),
    unpack_info = None
)

RESOURCES[Resource_Key.RIPEXT] = Resource(
    type = Resource_Type.EXTENSION,
    key = "ripext",
    name = "REST in Pawn Extension",
    install_dir = os.path.join(RESOURCES_EXTENSIONS_DIR_PATH, "ripext"),
    merge_paths = [],
    plugin_paths = [],
    download_info = resolve_download_info({
        OS_Type.WINDOWS: Download_Info(
            "https://github.com/ErikMinekus/sm-ripext/releases/download/1.3.2/sm-ripext-1.3.2-windows.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "ripext.zip")
        ),
        OS_Type.LINUX: Download_Info(
            "https://github.com/ErikMinekus/sm-ripext/releases/download/1.3.2/sm-ripext-1.3.2-linux.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "ripext.zip")
        )
    }),
    unpack_info = None
)

RESOURCES[Resource_Key.DYNAMIC_CHANNELS] = Resource(
    type = Resource_Type.PLUGIN,
    key = "dynamic_channels",
    name = "Dynamic Channels Plugin",
    install_dir = os.path.join(RESOURCES_PLUGINS_DIR_PATH, "dynamic_channels"),
    merge_paths = [],
    plugin_paths = [
        os.path.join(SCRIPTING_DIR_PATH, "DynamicChannels.sp"),
    ],
    download_info = resolve_download_info({
        get_os_type(): Download_Info(
            "https://github.com/Vauff/DynamicChannels/archive/refs/heads/master.zip",
            os.path.join(DOWNLOADS_DIR_PATH, "dynamic_channels.zip")
        )
    }),
    unpack_info = Unpack_Info(os.path.join("addons", "sourcemod"), True)
)

RESOURCES[Resource_Key.BHOPTIMER] = Resource(
    type = Resource_Type.PLUGIN,
    key = "bhoptimer",
    name = "Bhop Timer",
    install_dir = os.path.join(PLUGINS_DIR_PATH, "bhoptimer"),
    merge_paths = [],
    plugin_paths = [
        os.path.join(SCRIPTING_DIR_PATH, "eventqueuefix.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-chat.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-checkpoints.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-core.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-hud.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-mapchooser.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-misc.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-rankings.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-replay-playback.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-replay-recorder.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-sounds.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-stats.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-tas.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-timelimit.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-wr.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-zones.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "shavit-zones-json.sp")
    ],
    download_info = None,
    unpack_info = None
)

RESOURCES[Resource_Key.JUMPSTATS] = Resource(
    type = Resource_Type.PLUGIN,
    key = "jumpstats",
    name = "Jump Stats",
    install_dir = os.path.join(PLUGINS_DIR_PATH, "jumpstats"),
    merge_paths = [],
    plugin_paths = [
        os.path.join(SCRIPTING_DIR_PATH, "bhop-get-stats.sp"),
        os.path.join(SCRIPTING_DIR_PATH, "jumpstats.sp")
    ],
    include_paths = [
        os.path.join(RESOURCES[Resource_Key.DYNAMIC_CHANNELS].install_dir, SCRIPTING_DIR_PATH, "include"),
        os.path.join(RESOURCES[Resource_Key.BHOPTIMER].install_dir, SCRIPTING_DIR_PATH, "include")
    ],
    download_info = None,
    unpack_info = None
)

RESOURCES[Resource_Key.LANDFIX] = Resource(
    type = Resource_Type.PLUGIN,
    key = "landfix",
    name = "Land Fix",
    install_dir = os.path.join(PLUGINS_DIR_PATH, "landfix"),
    merge_paths = [],
    plugin_paths = [
        os.path.join(SCRIPTING_DIR_PATH, "landfix.sp")
    ],
    download_info = None,
    unpack_info = None
)

RESOURCES[Resource_Key.MAPLOADER] = Resource(
    type = Resource_Type.PLUGIN,
    key = "maploader",
    name = "Map Loader",
    install_dir = os.path.join(PLUGINS_DIR_PATH, "maploader"),
    merge_paths = [],
    plugin_paths = [
        os.path.join(SCRIPTING_DIR_PATH, "maploader.sp")
    ],
    include_paths = [
        os.path.join(RESOURCES[Resource_Key.BZIP2].install_dir, SCRIPTING_DIR_PATH, "include"),
        os.path.join(RESOURCES[Resource_Key.RIPEXT].install_dir, SCRIPTING_DIR_PATH, "include")
    ],
    download_info = None,
    unpack_info = None
)

RESOURCES[Resource_Key.PUSH_FIX_DE] = Resource(
    type = Resource_Type.PLUGIN,
    key = "push_fix_de",
    name = "PushFix Definitive Edition",
    install_dir = os.path.join(PLUGINS_DIR_PATH, "push_fix_de"),
    merge_paths = [],
    plugin_paths = [
        os.path.join(SCRIPTING_DIR_PATH, "pushfix_de.sp")
    ],
    download_info = None,
    unpack_info = None
)

RESOURCES[Resource_Key.RNGFIX] = Resource(
    type = Resource_Type.PLUGIN,
    key = "rngfix",
    name = "RNG Fix",
    install_dir = os.path.join(PLUGINS_DIR_PATH, "rngfix"),
    merge_paths = [],
    plugin_paths = [
        os.path.join(SCRIPTING_DIR_PATH, "rngfix.sp")
    ],
    download_info = None,
    unpack_info = None
)

RESOURCES[Resource_Key.SHOW_PLAYER_CLIPS] = Resource(
    type = Resource_Type.PLUGIN,
    key = "show_player_clips",
    name = "Show Player Clips",
    install_dir = os.path.join(PLUGINS_DIR_PATH, "show_player_clips"),
    merge_paths = [],
    plugin_paths = [
        os.path.join(SCRIPTING_DIR_PATH, "showplayerclips.sp")
    ],
    download_info = None,
    unpack_info = None
)

RESOURCES[Resource_Key.SHOWTRIGGERS] = Resource(
    type = Resource_Type.PLUGIN,
    key = "showtriggers",
    name = "Show Triggers",
    install_dir = os.path.join(PLUGINS_DIR_PATH, "showtriggers"),
    merge_paths = [],
    plugin_paths = [
        os.path.join(SCRIPTING_DIR_PATH, "showtriggers.sp")
    ],
    download_info = None,
    unpack_info = None
)

SOURCEMOD_RESOURCE = RESOURCES[Resource_Key.SOURCEMOD]
SOURCEMOD_RESOURCE_SCRIPTING_DIR_PATH = os.path.join(SOURCEMOD_RESOURCE.install_dir, SCRIPTING_DIR_PATH)

def get_sourcemod_spcomp_path():
    if get_os_type() == OS_Type.WINDOWS:
        return os.path.join(SOURCEMOD_RESOURCE_SCRIPTING_DIR_PATH, "spcomp64.exe")

    return os.path.join(SOURCEMOD_RESOURCE_SCRIPTING_DIR_PATH, "spcomp64")
