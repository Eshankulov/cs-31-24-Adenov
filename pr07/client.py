#!/usr/bin/env python3
"""Send one arithmetic expression to the FIFO server."""
import os
import uuid
from pathlib import Path
import argparse

BASE = Path("/tmp/os_pr07")
REQUEST_FIFO = BASE / "requests.fifo"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("expression", help='example: "2 * (3 + 4)"')
    a = p.parse_args()
    if not REQUEST_FIFO.exists(): p.error("server FIFO missing; start server.py first")
    client_id = uuid.uuid4().hex
    reply_fifo = BASE / f"reply_{client_id}.fifo"
    os.mkfifo(reply_fifo, 0o600)
    try:
        with REQUEST_FIFO.open("w", encoding="utf-8") as out:
            out.write(f"{client_id}|{a.expression}\n")
        with reply_fifo.open("r", encoding="utf-8") as inp:
            print(inp.readline().strip())
    finally:
        try: reply_fifo.unlink()
        except FileNotFoundError: pass

if __name__ == "__main__":
    main()
