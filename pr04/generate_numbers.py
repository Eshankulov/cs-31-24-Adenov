#!/usr/bin/env python3
"""Generate numbers.txt for the practical work."""
from pathlib import Path
import argparse

p = argparse.ArgumentParser()
p.add_argument("--count", type=int, default=1_000_000)
p.add_argument("--output", default="numbers.txt")
a = p.parse_args()
Path(a.output).write_text("".join(f"{i}\n" for i in range(1, a.count + 1)))
print(f"Created {a.output}: {a.count} integers")
