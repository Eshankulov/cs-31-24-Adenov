#!/usr/bin/env python3
"""Compare sequential, threaded and process-based CPU/I/O tasks."""
import argparse
import concurrent.futures as cf
import statistics
import time
import urllib.request
from pathlib import Path

def cpu_chunk(bounds):
    start, stop = bounds
    return sum(range(start, stop))

def cpu_sum(n, workers, mode):
    step = (n + workers - 1) // workers
    chunks = [(i, min(i + step, n)) for i in range(0, n, step)]
    if mode == "seq":
        return sum(cpu_chunk(c) for c in chunks)
    executor = cf.ThreadPoolExecutor if mode == "threads" else cf.ProcessPoolExecutor
    with executor(max_workers=workers) as pool:
        return sum(pool.map(cpu_chunk, chunks))

def fetch(url):
    with urllib.request.urlopen(url, timeout=5) as response:
        return len(response.read())

def timed(fn):
    start = time.perf_counter()
    value = fn()
    return time.perf_counter() - start, value

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=1_000_000, help="upper bound for CPU sum")
    parser.add_argument("--urls", default="urls.txt", help="file containing one URL per line")
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    print(f"CPU: sum(range({args.n})); workers=4; repeats={args.repeats}")
    for mode in ("seq", "threads", "processes"):
        times, result = [], None
        for _ in range(args.repeats):
            elapsed, result = timed(lambda: cpu_sum(args.n, 4, mode))
            times.append(elapsed)
        print(f"{mode:10s} median={statistics.median(times):.6f}s result={result}")
    urls_path = Path(args.urls)
    if not urls_path.exists():
        print(f"I/O skipped: create {urls_path} with one URL per line.")
        return
    urls = [line.strip() for line in urls_path.read_text().splitlines() if line.strip()]
    if not urls:
        print("I/O skipped: URL list is empty.")
        return
    print(f"I/O: {len(urls)} URLs; repeats={args.repeats}")
    for mode in ("seq", "threads", "processes"):
        times, result = [], None
        for _ in range(args.repeats):
            if mode == "seq":
                fn = lambda: [fetch(url) for url in urls]
            else:
                executor = cf.ThreadPoolExecutor if mode == "threads" else cf.ProcessPoolExecutor
                fn = lambda executor=executor: list(executor(max_workers=4).map(fetch, urls))
            elapsed, result = timed(fn)
            times.append(elapsed)
        print(f"{mode:10s} median={statistics.median(times):.6f}s bytes={sum(result)}")

if __name__ == "__main__":
    main()
