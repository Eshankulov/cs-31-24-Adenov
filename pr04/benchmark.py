#!/usr/bin/env python3
"""Compare sequential, threaded and process-based work for Practical Work 4."""
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
from statistics import median
from time import perf_counter
from urllib.request import urlopen
import argparse
import os

ROOT = Path(__file__).resolve().parent

def sum_chunk(values):
    return sum(values)

def load_numbers(path):
    with path.open("r", encoding="utf-8") as file:
        return [int(line) for line in file if line.strip()]

def chunks(values, count):
    size = (len(values) + count - 1) // count
    return [values[i:i + size] for i in range(0, len(values), size)]

def measure(label, operation, repeats=3):
    samples = []
    result = None
    for _ in range(repeats):
        start = perf_counter()
        result = operation()
        samples.append(perf_counter() - start)
    print(f"{label:<24} median={median(samples):8.3f}s  runs="
          + ", ".join(f"{x:.3f}" for x in samples))
    return result, median(samples)

def cpu_benchmark(path):
    values = load_numbers(path)
    pieces = chunks(values, 4)
    expected = sum(values)
    print(f"Numbers: {len(values):,}; CPU cores visible: {os.cpu_count()}")
    print("All timings use the median of 3 runs; file loading is outside timing.")

    results = {}
    result, results["one thread"] = measure("One thread", lambda: sum(values))
    assert result == expected

    def threaded():
        with ThreadPoolExecutor(max_workers=4) as pool:
            return sum(pool.map(sum_chunk, pieces))
    result, results["4 threads"] = measure("4 threads", threaded)
    assert result == expected

    def processes():
        with ProcessPoolExecutor(max_workers=4) as pool:
            return sum(pool.map(sum_chunk, pieces))
    result, results["4 processes"] = measure("4 processes", processes)
    assert result == expected

    print(f"Verified sum: {expected:,}")
    return results

def fetch_size(url):
    with urlopen(url, timeout=10) as response:
        return len(response.read())

def network_benchmark(base_url):
    urls = [f"{base_url.rstrip('/')}/file{i:02d}.txt" for i in range(1, 21)]
    print("\nNetwork I/O test: 20 local HTTP URLs")
    results = {}

    sequential_result, results["sequential"] = measure(
        "Sequential", lambda: [fetch_size(url) for url in urls])

    def threaded():
        with ThreadPoolExecutor(max_workers=4) as pool:
            return list(pool.map(fetch_size, urls))
    threaded_result, results["ThreadPoolExecutor"] = measure("ThreadPoolExecutor", threaded)

    def processes():
        with ProcessPoolExecutor(max_workers=4) as pool:
            return list(pool.map(fetch_size, urls))
    process_result, results["ProcessPoolExecutor"] = measure("ProcessPoolExecutor", processes)

    assert sequential_result == threaded_result == process_result, "Fetched file sizes differ"
    print("All three approaches fetched the same 20 files.")
    return results

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--numbers", type=Path, default=ROOT / "numbers.txt")
    parser.add_argument("--network", action="store_true",
                        help="also benchmark 20 local HTTP files")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000",
                        help="base URL of the local HTTP server")
    args = parser.parse_args()

    if not args.numbers.exists():
        raise SystemExit(f"Missing {args.numbers}. Run: python3 {ROOT / 'prepare_data.py'}")
    cpu_benchmark(args.numbers)
    if args.network:
        network_benchmark(args.base_url)

if __name__ == "__main__":
    main()
