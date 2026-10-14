#!/usr/bin/env python3
"""Generate numbers.txt and 20 small files for the practical work."""
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10_000_000,
                        help="number of integers to write (default: 10 million)")
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count must be positive")

    root = Path(__file__).resolve().parent
    numbers_path = root / "numbers.txt"
    print(f"Creating {numbers_path} with {args.count:,} integers...")
    with numbers_path.open("w", encoding="utf-8") as file:
        for start in range(0, args.count, 10_000):
            end = min(start + 10_000, args.count)
            file.write("\n".join(str(n) for n in range(start + 1, end + 1)))
            file.write("\n")

    data_dir = root / "web_data"
    data_dir.mkdir(exist_ok=True)
    for i in range(1, 21):
        (data_dir / f"file{i:02d}.txt").write_text(
            f"Sample response body for file {i}.\n" * 100,
            encoding="utf-8"
        )
    print("Done: numbers.txt and 20 files in web_data/.")

if __name__ == "__main__":
    main()
