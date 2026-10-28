#!/usr/bin/env python3
"""Banker's algorithm: safety check and request handling with rollback."""
import argparse
import json
from copy import deepcopy
from pathlib import Path

def safety(available, allocation, maximum):
    n, m = len(allocation), len(available)
    need = [[maximum[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]
    work, finish, sequence = available[:], [False] * n, []
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                work = [work[j] + allocation[i][j] for j in range(m)]
                finish[i] = True
                sequence.append(i)
                changed = True
    return all(finish), sequence, need

def request(available, allocation, maximum, pid, vector):
    if pid < 0 or pid >= len(allocation): raise ValueError("unknown process")
    need = [maximum[pid][j] - allocation[pid][j] for j in range(len(available))]
    if any(x < 0 for x in vector): raise ValueError("request cannot be negative")
    if any(vector[j] > need[j] for j in range(len(vector))): return False, "request exceeds Need"
    if any(vector[j] > available[j] for j in range(len(vector))): return False, "not enough Available resources"
    old_av, old_al = available[:], deepcopy(allocation)
    for j, value in enumerate(vector):
        available[j] -= value
        allocation[pid][j] += value
    safe, seq, _ = safety(available, allocation, maximum)
    if not safe:
        available[:] = old_av
        allocation[:] = old_al
        return False, "unsafe state; changes rolled back"
    return True, "safe sequence: " + " -> ".join(f"P{i}" for i in seq)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file", help="JSON file with available, allocation, maximum")
    a = p.parse_args()
    data = json.loads(Path(a.file).read_text())
    available, allocation, maximum = data["available"], data["allocation"], data["maximum"]
    safe, seq, need = safety(available, allocation, maximum)
    print("Need =", need)
    print("SAFE" if safe else "UNSAFE", "sequence:", " -> ".join(f"P{i}" for i in seq) if safe else "-")
    print("Enter request as: PID r1 r2 r3; Ctrl+D to finish")
    for line in __import__("sys").stdin:
        parts = line.split()
        if len(parts) != len(available) + 1: print("invalid request format"); continue
        try:
            ok, message = request(available, allocation, maximum, int(parts[0]), list(map(int, parts[1:])))
            print(("GRANTED: " if ok else "DENIED: ") + message)
        except (ValueError, IndexError) as exc: print(f"ERROR: {exc}")

if __name__ == "__main__":
    main()
