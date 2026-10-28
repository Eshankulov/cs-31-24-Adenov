#!/usr/bin/env python3
"""Intentionally unsynchronized shared counter for comparison."""
import threading
counter=0
def worker():
    global counter
    for _ in range(100_000):
        counter += 1
threads=[threading.Thread(target=worker) for _ in range(4)]
for t in threads:t.start()
for t in threads:t.join()
print(f"counter={counter}; expected=400000; result may vary by runtime")
