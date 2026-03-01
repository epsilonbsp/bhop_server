# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 EpsilonBSP

from enum import auto, IntEnum
import os
import shutil
import sys
import tarfile
import zipfile

class Unpack_Status(IntEnum):
    SUCCESS = auto()
    FAILURE = auto()

def unpack_file(archive_path: str, unpack_path: str, strip_top_level: bool = False) -> tuple[Unpack_Status, Exception | None]:
    try:
        if zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path, "r") as archive:
                archive.extractall(unpack_path)
        elif tarfile.is_tarfile(archive_path):
            with tarfile.open(archive_path, "r:*") as archive:
                archive.extractall(unpack_path)
        else:
            raise Exception("Unsupported archive type")

        if strip_top_level:
            items = [
                os.path.join(unpack_path, item)
                for item in os.listdir(unpack_path)
            ]

            if len(items) == 1 and os.path.isdir(items[0]):
                top_folder = items[0]

                for item in os.listdir(top_folder):
                    shutil.move(
                        os.path.join(top_folder, item),
                        unpack_path
                    )

                os.rmdir(top_folder)

        return Unpack_Status.SUCCESS, None
    except Exception as e:
        return Unpack_Status.FAILURE, e

def unpack_file_and_log(name: str, archive_path: str, unpack_path: str, strip_top_level: bool = False) -> None:
    print(f"Unpacking {name}...")
    print(f"From: {os.path.abspath(archive_path)}")
    print(f"To: {os.path.abspath(unpack_path)}")

    status, e = unpack_file(archive_path, unpack_path, strip_top_level)

    if status == Unpack_Status.SUCCESS:
        print("Unpacking success!")
    else:
        print(f"Unpacking failure: {e}")
        sys.exit(1)
