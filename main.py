#!/usr/bin/env python3
"""Sum up 26 November's world news in one image — make.fun entry.

Copies the built news poster (news26.png) to /output/entry.png
(or $MAKEFUN_OUTPUT_DIR/entry.png) and validates it:
PNG magic + IEND, at most 1 MiB, at most 1024x1024 pixels.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "news26.png")
MAX_BYTES = 1048576
MAX_DIM = 1024


def main() -> int:
    if not os.path.exists(SRC):
        print(f"missing image: {SRC}", file=sys.stderr)
        return 1
    with open(SRC, "rb") as f:
        data = f.read()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        print("not a PNG file", file=sys.stderr)
        return 1
    if b"IEND" not in data[-16:]:
        print("PNG is truncated (no IEND)", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"image is {len(data)} bytes, over the 1 MiB limit", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        print(f"image is {width}x{height}, over the 1024x1024 limit", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)
    print(f"wrote entry.png ({width}x{height}, {len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
