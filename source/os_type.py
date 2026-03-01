# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 EpsilonBSP

from enum import auto, IntEnum
import sys

class OS_Type(IntEnum):
    WINDOWS = auto()
    LINUX = auto()

def get_os_type() -> OS_Type:
    if sys.platform == "win32":
        return OS_Type.WINDOWS

    if sys.platform == "linux":
        return OS_Type.LINUX

    return 0
