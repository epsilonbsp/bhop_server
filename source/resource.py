# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 EpsilonBSP

from dataclasses import dataclass, field
from typing import List

from .os_type import *

@dataclass
class Download_Info:
    url: str
    path: str

@dataclass
class Unpack_Info:
    wrapper_path: str = ""
    strip_top_level: bool = False

class Resource_Type(IntEnum):
    CORE = auto()
    EXTENSION = auto()
    PLUGIN = auto()

@dataclass
class Resource:
    type: Resource_Type
    key: str
    name: str
    install_dir: str
    merge_paths: List[str]
    plugin_paths: List[str]
    include_paths: List[str] = field(default_factory = list)
    download_info: Download_Info|None = None
    unpack_info: Unpack_Info|None = None

def resolve_download_info(list: dict[OS_Type, Download_Info]) -> None:
    os_type = get_os_type()

    if os_type not in list:
        return None

    return list[os_type]
