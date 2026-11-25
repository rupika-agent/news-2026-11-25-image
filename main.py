"""Write the 25 November 2026 world-news image to the output directory.

The image is drawn once, shipped in this repository as ``entry.png``,
and this program copies it byte for byte to ``/output/entry.png``,
so every run produces identical bytes.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(out_dir) / "entry.png"


PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def sha256_of(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1 << 20)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not SOURCE.is_file():
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    with SOURCE.open("rb") as handle:
        if handle.read(len(PNG_MAGIC)) != PNG_MAGIC:
            print("entry.png is not a PNG file", file=sys.stderr)
            return 1
    dest = output_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, dest)
    before = sha256_of(SOURCE)
    after = sha256_of(dest)
    if before != after:
        print("copy mismatch", file=sys.stderr)
        return 1
    print(after)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
