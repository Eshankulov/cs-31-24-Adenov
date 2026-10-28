#!/usr/bin/env python3
"""Build the current user's process tree from /proc without using ps."""
from pathlib import Path
import os

PROC=Path("/proc")
def details(pid):
    try:
        raw=(PROC/str(pid)/"stat").read_text(); end=raw.rfind(")")
        name=raw[raw.find("(")+1:end]; fields=raw[end+2:].split()
        state,ppid=fields[0],int(fields[1])
        status=(PROC/str(pid)/"status").read_text()
        uid_line=next(x for x in status.splitlines() if x.startswith("Uid:"))
        uid=int(uid_line.split()[1])
        rss_line=next((x for x in status.splitlines() if x.startswith("VmRSS:")),"VmRSS: 0 kB")
        rss=int(rss_line.split()[1])
        return uid,ppid,name,state,rss
    except (OSError,ValueError,IndexError,StopIteration): return None
def main():
    uid=os.getuid(); procs={}
    for item in PROC.iterdir():
        if item.name.isdigit():
            pid=int(item.name); d=details(pid)
            if d and d[0]==uid: procs[pid]=d[1:]
    children={}
    for pid,(ppid,*_) in procs.items(): children.setdefault(ppid,[]).append(pid)
    roots=sorted(pid for pid,(ppid,*_) in procs.items() if ppid not in procs)
    def show(pid,prefix="",last=True):
        ppid,name,state,rss=procs[pid]
        print(f"{prefix}{'└─ ' if last else '├─ '}PID={pid} PPID={ppid} state={state} RSS={rss} kB {name}")
        kids=sorted(children.get(pid,[]))
        for i,kid in enumerate(kids): show(kid,prefix+("   " if last else "│  "),i==len(kids)-1)
    for i,pid in enumerate(roots): show(pid,"",i==len(roots)-1)
if __name__=="__main__": main()
