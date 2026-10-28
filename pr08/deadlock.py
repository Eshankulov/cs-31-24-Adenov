#!/usr/bin/env python3
"""Intentionally unsafe lock ordering; run only as a short demonstration."""
import threading, time
a=threading.Lock(); b=threading.Lock()
def first():
    with a:
        print("T1 acquired A; waiting for B",flush=True); time.sleep(.1)
        with b: print("T1 acquired A and B")
def second():
    with b:
        print("T2 acquired B; waiting for A",flush=True); time.sleep(.1)
        with a: print("T2 acquired B and A")
if __name__=="__main__":
    x=threading.Thread(target=first,daemon=True); y=threading.Thread(target=second,daemon=True)
    x.start(); y.start(); x.join(timeout=1); y.join(timeout=1)
    print("Potential deadlock detected by timeout:",x.is_alive() and y.is_alive())
