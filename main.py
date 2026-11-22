"""Ship the finished front page to the make.fun output folder.

The page is rendered offline by build.py (Pillow) and committed as
entry.png; this file only copies it byte-for-byte into
$MAKEFUN_OUTPUT_DIR (default /output). Standard library only —
it never imports build.py, so it runs in the stdlib-only sandbox.
"""

import hashlib
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
MAX_BYTES = 1024 * 1024  # entry limit: 1 MiB


def png_size(path):
    """Read width/height from the PNG IHDR chunk (stdlib only)."""
    with open(path, "rb") as f:
        header = f.read(24)
    assert header[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG file"
    assert header[12:16] == b"IHDR", "missing IHDR chunk"
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def deliver():
    src = os.path.join(HERE, "entry.png")
    # Verify the committed file before shipping it: real PNG,
    # 1024x1024, within the 1 MiB limit. Failing here is better
    # than shipping a bad file to the grader.
    width, height = png_size(src)
    assert (width, height) == (1024, 1024), f"bad size {width}x{height}"
    size = os.path.getsize(src)
    assert size <= MAX_BYTES, f"entry.png is {size} bytes (> 1 MiB)"
    with open(src, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    os.makedirs(DEST, exist_ok=True)
    shutil.copyfile(src, os.path.join(DEST, "entry.png"))
    print(f"delivered entry.png to {DEST} "
          f"({width}x{height}, {size} bytes, sha256 {digest[:16]}…)")


if __name__ == "__main__":
    deliver()
