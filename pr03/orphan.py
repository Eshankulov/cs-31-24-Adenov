#!/usr/bin/env python3
"""Create a child that outlives its parent briefly and print its new PPID."""
import os, time
pid=os.fork()
if pid==0:
    time.sleep(2)
    print(f"Orphan child PID={os.getpid()} adopted by PPID={os.getppid()}",flush=True)
    time.sleep(2)
    os._exit(0)
print(f"Parent PID={os.getpid()} exits; child PID={pid} should be adopted.",flush=True)
os._exit(0)
