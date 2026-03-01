# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 EpsilonBSP

import os
import shutil

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

def clear_dir(path: str) -> None:
    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
