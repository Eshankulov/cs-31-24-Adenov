#!/usr/bin/env python3
"""Observe RSS before/after modifying a large inherited list after fork."""
import os, time

def rss_kb():
    try:
        for line in open("/proc/self/status"):
            if line.startswith("VmRSS:"): return int(line.split()[1])
    except OSError: pass
    return -1

def main():
    data=list(range(2_000_000))
    print(f"Parent RSS before fork: {rss_kb()} kB",flush=True)
    pid=os.fork()
    if pid==0:
        print(f"Child RSS before mutation: {rss_kb()} kB",flush=True)
        for i in range(0,len(data),100): data[i]=-data[i]
        print(f"Child RSS after mutation: {rss_kb()} kB",flush=True)
        os._exit(0)
    os.waitpid(pid,0)
    print(f"Parent RSS after child exits: {rss_kb()} kB")
if __name__=="__main__": main()
