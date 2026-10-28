#!/usr/bin/env python3
"""Counter protected by a mutex."""
import threading
counter=0
lock=threading.Lock()
def worker():
    global counter
    for _ in range(100_000):
        with lock: counter += 1
threads=[threading.Thread(target=worker) for _ in range(4)]
for t in threads:t.start()
for t in threads:t.join()
print(f"counter={counter}; expected=400000")
assert counter==400_000
