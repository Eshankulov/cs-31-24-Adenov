#!/usr/bin/env python3
"""Start N children with fork/exec, wait for all, and report exit codes and elapsed time."""
import argparse, os, time

def main():
    p=argparse.ArgumentParser()
    p.add_argument("-n","--count",type=int,default=3)
    p.add_argument("command",nargs=argparse.REMAINDER,help="command after --, e.g. -- /bin/sleep 1")
    a=p.parse_args()
    command=a.command[1:] if a.command and a.command[0]=="--" else a.command
    if a.count<1 or not command: p.error("use --count N -- COMMAND [ARGS...]")
    starts={}; pids=[]
    for _ in range(a.count):
        start=time.perf_counter(); pid=os.fork()
        if pid==0:
            try: os.execvp(command[0],command)
            except OSError as e:
                print(f"exec failed: {e}",flush=True); os._exit(127)
        starts[pid]=start; pids.append(pid)
    remaining=set(pids)
    while remaining:
        pid,status=os.wait()
        if pid not in remaining: continue
        remaining.remove(pid)
        code=os.waitstatus_to_exitcode(status)
        print(f"PID={pid} exit={code} elapsed={time.perf_counter()-starts[pid]:.3f}s")
if __name__=="__main__": main()
