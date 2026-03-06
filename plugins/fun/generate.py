# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 EpsilonBSP

import os
import sys
import wave
import struct

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR   = os.path.join(SCRIPT_DIR, "sound", "fun")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "addons", "sourcemod", "configs", "fun_sounds.cfg")
EXTENSIONS  = {".mp3", ".wav", ".ogg"}

def wav_duration(path):
    with wave.open(path, "rb") as w:
        return w.getnframes() / w.getframerate()

def mp3_duration(path):
    size = os.path.getsize(path)

    with open(path, "rb") as f:
        # Skip ID3v2 tag if present
        tag_offset = 0
        magic = f.read(3)

        if magic == b"ID3":
            f.seek(6)
            b = f.read(4)
            # Syncsafe integer
            tag_offset = 10 + ((b[0] << 21) | (b[1] << 14) | (b[2] << 7) | b[3])

        f.seek(tag_offset)

        # Scan for first valid MPEG sync frame
        buf = f.read(8192)
        BITRATES_V1L3 = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0]
        BITRATES_V1L2 = [0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384, 0]
        BITRATES_V2L3 = [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0]

        for i in range(len(buf) - 3):
            if buf[i] != 0xFF or (buf[i+1] & 0xE0) != 0xE0:
                continue

            b1, b2 = buf[i+1], buf[i+2]
            ver   = (b1 >> 3) & 0x3 # 3=MPEG1, 2=MPEG2, 0=MPEG2.5
            layer = (b1 >> 1) & 0x3 # 1=L3, 2=L2, 3=L1
            bri   = (b2 >> 4) & 0xF
            sri   = (b2 >> 2) & 0x3

            if sri == 3 or bri in (0, 15):
                continue

            if ver == 3 and layer == 1:
                bitrate = BITRATES_V1L3[bri] * 1000
            elif ver == 3 and layer == 2:
                bitrate = BITRATES_V1L2[bri] * 1000
            elif ver in (2, 0) and layer == 1:
                bitrate = BITRATES_V2L3[bri] * 1000
            else:
                continue

            if bitrate == 0:
                continue

            return (size - tag_offset) * 8 / bitrate

    # Fallback: estimate at 128 kbps
    return size / 16000.0

def ogg_duration(path):
    with open(path, "rb") as f:
        # Read first Ogg page to get Vorbis sample rate
        if f.read(4) != b"OggS":
            return -1.0

        f.seek(6)
        f.seek(f.tell() + 8 + 4 + 4 + 4) # skip granule, serial, seq, checksum

        num_segs = struct.unpack("B", f.read(1))[0]
        seg_table = f.read(num_segs)
        page_data_size = sum(seg_table)
        vorbis_hdr = f.read(page_data_size)

        if vorbis_hdr[:7] != b"\x01vorbis":
            return -1.0

        sample_rate = struct.unpack("<I", vorbis_hdr[11:15])[0]

        if sample_rate == 0:
            return -1.0

        # Read last chunk of file to find highest granule position
        f.seek(0, 2)
        file_size = f.tell()
        f.seek(max(0, file_size - 65536))
        tail = f.read()

        last_granule = 0
        pos = 0

        while True:
            idx = tail.find(b"OggS", pos)

            if idx == -1 or idx + 14 > len(tail):
                break

            granule = struct.unpack("<q", tail[idx + 6 : idx + 14])[0]

            if granule > 0:
                last_granule = granule

            pos = idx + 1

        if last_granule > 0:
            return last_granule / sample_rate

    return -1.0


DURATION_FN = {
    ".wav": wav_duration,
    ".mp3": mp3_duration,
    ".ogg": ogg_duration
}

def main():
    if not os.path.isdir(SOUND_DIR):
        sys.exit(f"Sound directory not found: {SOUND_DIR}")

    entries = []

    for fname in sorted(os.listdir(SOUND_DIR)):
        name, ext = os.path.splitext(fname)

        if ext.lower() not in EXTENSIONS:
            continue

        fpath = os.path.join(SOUND_DIR, fname)

        try:
            duration = DURATION_FN[ext.lower()](fpath)
        except Exception as e:
            print(f"  WARNING: {fname}: {e}, skipping")

            continue

        if duration <= 0:
            print(f"WARNING: could not read duration for {fname}, skipping")

            continue

        entries.append((name, fname, duration))
        print(f"{fname}: {duration:.2f}s")

    if not entries:
        sys.exit("No audio files found.")

    lines = ['"FunSounds"\n{\n']

    for key, fname, duration in entries:
        lines.append(f'    "{key}"\n')
        lines.append( '    {\n')
        lines.append(f'        "file"      "{fname}"\n')
        lines.append(f'        "duration"  "{duration:.2f}"\n')
        lines.append( '    }\n')

    lines.append('}\n')

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok = True)

    with open(OUTPUT_PATH, "w") as f:
        f.writelines(lines)

    print(f"\nWrote {len(entries)} entries to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
