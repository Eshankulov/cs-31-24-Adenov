#!/usr/bin/env python3
"""Detect cycles in a wait-for graph built from acquire/release/wait event logs."""
import argparse

def detect(path):
    owner, waits = {}, {}
    with open(path, encoding="utf-8") as f:
        for raw in f:
            parts = raw.split()
            if len(parts) != 3: continue
            event, thread, lock = parts
            if event == "acquire":
                if lock in owner and owner[lock] != thread:
                    waits.setdefault(thread, set()).add(owner[lock])
                else: owner[lock] = thread
            elif event == "release":
                if owner.get(lock) == thread: owner.pop(lock, None)
                waits.pop(thread, None)
            elif event == "wait" and lock in owner and owner[lock] != thread:
                waits.setdefault(thread, set()).add(owner[lock])
    visiting, visited, stack = set(), set(), []
    def dfs(node):
        if node in visiting: return stack[stack.index(node):] + [node]
        if node in visited: return None
        visiting.add(node); stack.append(node)
        for nxt in waits.get(node, ()):
            cycle = dfs(nxt)
            if cycle: return cycle
        stack.pop(); visiting.remove(node); visited.add(node)
        return None
    for node in waits:
        cycle = dfs(node)
        if cycle: return cycle, waits
    return None, waits

if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("log", nargs="?", default="events.txt"); a=p.parse_args()
    cycle, graph=detect(a.log)
    print("Wait-for graph:", {k:sorted(v) for k,v in graph.items()})
    print("DEADLOCK: "+" -> ".join(cycle) if cycle else "No cycle detected")
