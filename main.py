#!/usr/bin/env python3
"""Copy the generated front page (entry.png) to the make.fun output dir.

Pure Python standard library only. No network, no side effects beyond
the single copy. Deterministic: the output bytes are exactly the bytes
of entry.png next to this script.

Usage:
    MAKEFUN_OUTPUT_DIR=/path/to/out python3 main.py
"""

import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found; run tools/build_image.py first",
              file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
