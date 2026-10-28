#!/usr/bin/env python3
"""Display a process tree by reading /proc on Linux."""
from pathlib import Path

PROC = Path("/proc")

def read_process(pid: int):
    try:
        raw = (PROC / str(pid) / "stat").read_text()
        # comm may contain spaces and parentheses; fields after the final ')' start with state, ppid.
        end = raw.rfind(")")
        name = raw[raw.find("(") + 1:end]
        fields = raw[end + 2:].split()
        state, ppid = fields[0], int(fields[1])
        return ppid, name, state
    except (OSError, ValueError, IndexError):
        return None

def main():
    processes = {}
    for item in PROC.iterdir():
        if item.name.isdigit():
            pid = int(item.name)
            info = read_process(pid)
            if info:
                ppid, name, state = info
                processes[pid] = (ppid, name, state)
    children = {}
    for pid, (ppid, _, _) in processes.items():
        children.setdefault(ppid, []).append(pid)
    for values in children.values():
        values.sort()
    roots = sorted(pid for pid, (ppid, _, _) in processes.items() if ppid not in processes)
    def show(pid, prefix="", last=True):
        ppid, name, state = processes[pid]
        print(f"{prefix}{'└─ ' if last else '├─ '}{name} [PID={pid}, PPID={ppid}, state={state}]")
        kids = children.get(pid, [])
        for i, child in enumerate(kids):
            show(child, prefix + ("   " if last else "│  "), i == len(kids) - 1)
    for i, pid in enumerate(roots):
        show(pid, "", i == len(roots) - 1)

if __name__ == "__main__":
    main()
