#!/usr/bin/env python3
"""Demonstrate wait-for cycle detection before blocking."""
import threading

class DeadlockDetected(RuntimeError): pass

class LockGraph:
    def __init__(self):
        self.guard=threading.Lock(); self.owner={}; self.waits={}
    def would_cycle(self, waiter, owner):
        self.waits[waiter]=owner
        current=owner; seen={waiter}
        while current in self.waits:
            if current in seen:
                self.waits.pop(waiter,None)
                return True
            seen.add(current); current=self.waits[current]
        return False

class TrackedLock:
    def __init__(self, name, graph):
        self.name=name; self.graph=graph; self.lock=threading.Lock()
    def acquire(self):
        tid=threading.current_thread().name
        with self.graph.guard:
            owner=self.graph.owner.get(self.name)
            if owner is not None and owner != tid and self.graph.would_cycle(tid,owner):
                raise DeadlockDetected(f"cycle detected: {tid} waits for {self.name}, owned by {owner}")
        self.lock.acquire()
        with self.graph.guard:
            self.graph.waits.pop(tid,None); self.graph.owner[self.name]=tid
    def release(self):
        tid=threading.current_thread().name
        with self.graph.guard:
            if self.graph.owner.get(self.name)==tid: self.graph.owner.pop(self.name,None)
        self.lock.release()
    def __enter__(self): self.acquire(); return self
    def __exit__(self, exc_type, exc, tb): self.release(); return False

if __name__=="__main__":
    graph=LockGraph()
    graph.waits["T1"]="T2"
    if graph.would_cycle("T2","T1"): print("DEADLOCK detected: T1 -> T2 -> T1")
    else: print("No cycle")
