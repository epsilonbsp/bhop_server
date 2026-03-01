# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 EpsilonBSP

from enum import auto, IntEnum
import os
import sys
from typing import Callable
import urllib.request

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
            content_length = response.headers.get("Content-Length")

            downloaded_size = 0
            total_size = int(content_length) if content_length else 0

            os.makedirs(os.path.dirname(path), exist_ok = True)

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
        if total_size <= 0:
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
