#!/usr/bin/env python3
"""Demonstrate fork/exec/wait and child process status on Linux."""
import os
import sys

def main():
    print(f"Родитель: PID={os.getpid()}, PPID={os.getppid()}", flush=True)
    pid = os.fork()
    if pid == 0:
        print(f"Ребёнок до exec: PID={os.getpid()}, PPID={os.getppid()}", flush=True)
        os.execlp("sh", "sh", "-c", 'echo "Ребёнок после exec: PID=$$"; exit 7')
    waited_pid, status = os.waitpid(pid, 0)
    code = os.waitstatus_to_exitcode(status)
    print(f"Родитель дождался PID={waited_pid}, код завершения={code}")
    return 0 if code == 7 else 1

if __name__ == "__main__":
    raise SystemExit(main())
