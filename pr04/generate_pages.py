#!/usr/bin/env python3
from pathlib import Path
root = Path("webdata")
root.mkdir(exist_ok=True)
for i in range(20):
    (root / f"page{i:02d}.txt").write_text((f"Local benchmark page {i}\n") * (i + 1))
print("Created 20 pages in webdata/")
print("Run: python3 -m http.server 8000 --directory webdata")
print("URLs are in urls.txt; keep server running in another terminal.")
