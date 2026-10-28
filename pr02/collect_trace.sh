#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v strace >/dev/null || { echo "Install strace first: sudo apt install strace" >&2; exit 2; }
python3 hello.py data/example.log
strace -f -o trace.txt python3 hello.py data/example.log
strace -c cat data/example.log 2>cat_trace_summary.txt
strace -c python3 hello.py data/example.log 2>python_trace_summary.txt
echo "Created trace.txt, cat_trace_summary.txt, python_trace_summary.txt"
