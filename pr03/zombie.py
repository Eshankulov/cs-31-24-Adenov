#!/usr/bin/env python3
"""Create a child that exits while parent delays wait(), exposing a zombie."""
import os, time
pid=os.fork()
if pid==0:
    print(f"Child PID={os.getpid()} exiting now",flush=True); os._exit(0)
print(f"Parent PID={os.getpid()}, child PID={pid}; inspect with: ps -o pid,ppid,stat,cmd -p {pid}")
time.sleep(15)
os.waitpid(pid,0)
print("Parent collected child status; zombie is gone.")
