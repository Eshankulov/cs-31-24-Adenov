#!/usr/bin/env python3
"""Print a file's size in bytes."""
import argparse
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="path to the file")
    args = parser.parse_args()
    path = Path(args.file)
    try:
        print(f"{path.stat().st_size}")
    except OSError as exc:
        parser.error(str(exc))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
