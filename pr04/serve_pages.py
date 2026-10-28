#!/usr/bin/env python3
"""Serve local benchmark pages concurrently for the I/O experiment."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parent/"webdata"
ROOT.mkdir(exist_ok=True)
os.chdir(ROOT)
server=ThreadingHTTPServer(("127.0.0.1",8000),SimpleHTTPRequestHandler)
print("Threaded test server: http://127.0.0.1:8000",flush=True)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
finally:
    server.server_close()
