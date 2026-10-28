#!/usr/bin/env python3
"""Deadlock avoided by acquiring both locks in the same global order."""
import threading
a=threading.Lock(); b=threading.Lock()
def worker(name):
    with a:
        with b: print(f"{name}: acquired A then B")
threads=[threading.Thread(target=worker,args=(f"T{i}",)) for i in range(1,3)]
for t in threads:t.start()
for t in threads:t.join()
print("Completed without deadlock")
