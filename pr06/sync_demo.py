#!/usr/bin/env python3
"""Ring buffer using semaphores or a condition variable, plus a reusable barrier."""
import argparse
import threading
from collections import Counter

CAPACITY = 5
PRODUCERS = 3
CONSUMERS = 2
PER_PRODUCER = 1000

class SemaphoreRing:
    def __init__(self, capacity):
        self.data = [None] * capacity
        self.capacity = capacity
        self.read_i = self.write_i = 0
        self.mutex = threading.Lock()
        self.empty = threading.Semaphore(capacity)
        self.full = threading.Semaphore(0)
        self.size = 0
        self.max_size = 0
    def put(self, item):
        self.empty.acquire()
        with self.mutex:
            self.data[self.write_i] = item
            self.write_i = (self.write_i + 1) % self.capacity
            self.size += 1
            self.max_size = max(self.max_size, self.size)
        self.full.release()
    def get(self):
        self.full.acquire()
        with self.mutex:
            item = self.data[self.read_i]
            self.data[self.read_i] = None
            self.read_i = (self.read_i + 1) % self.capacity
            self.size -= 1
            return item

class ConditionRing:
    def __init__(self, capacity):
        self.data = [None] * capacity
        self.capacity = capacity
        self.read_i = self.write_i = self.size = 0
        self.cv = threading.Condition()
        self.max_size = 0
    def put(self, item):
        with self.cv:
            while self.size == self.capacity:
                self.cv.wait()
            self.data[self.write_i] = item
            self.write_i = (self.write_i + 1) % self.capacity
            self.size += 1
            self.max_size = max(self.max_size, self.size)
            self.cv.notify_all()
    def get(self):
        with self.cv:
            while self.size == 0:
                self.cv.wait()
            item = self.data[self.read_i]
            self.data[self.read_i] = None
            self.read_i = (self.read_i + 1) % self.capacity
            self.size -= 1
            self.cv.notify_all()
            return item

def run(mode):
    ring = SemaphoreRing(CAPACITY) if mode == "semaphore" else ConditionRing(CAPACITY)
    output, out_lock = [], threading.Lock()
    sentinel = object()
    def producer(index):
        for seq in range(PER_PRODUCER):
            ring.put((index, seq))
    def consumer():
        while True:
            item = ring.get()
            if item is sentinel:
                return
            with out_lock:
                output.append(item)
    consumers = [threading.Thread(target=consumer) for _ in range(CONSUMERS)]
    producers = [threading.Thread(target=producer, args=(i,)) for i in range(PRODUCERS)]
    for t in consumers + producers: t.start()
    for t in producers: t.join()
    for _ in consumers: ring.put(sentinel)
    for t in consumers: t.join()
    counts = Counter(output)
    expected = PRODUCERS * PER_PRODUCER
    duplicates = sum(n - 1 for n in counts.values() if n > 1)
    print(f"mode={mode} consumed={len(output)} expected={expected} unique={len(counts)} duplicates={duplicates} max_buffer={ring.max_size}")
    assert len(output) == expected and len(counts) == expected and duplicates == 0
    assert ring.max_size <= CAPACITY

class ReusableBarrier:
    def __init__(self, parties):
        self.parties = parties
        self.count = 0
        self.generation = 0
        self.cv = threading.Condition()
    def wait(self):
        with self.cv:
            gen = self.generation
            self.count += 1
            if self.count == self.parties:
                self.count = 0
                self.generation += 1
                self.cv.notify_all()
            else:
                while gen == self.generation:
                    self.cv.wait()

def barrier_demo():
    barrier = ReusableBarrier(4)
    def worker(i):
        for phase in range(1, 4):
            print(f"thread {i}: phase {phase} start")
            barrier.wait()
            print(f"thread {i}: phase {phase} complete")
            barrier.wait()
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["semaphore", "condition", "both", "barrier"], default="both")
    a = p.parse_args()
    if a.mode in ("semaphore", "both"): run("semaphore")
    if a.mode in ("condition", "both"): run("condition")
    if a.mode == "barrier": barrier_demo()
