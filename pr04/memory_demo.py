#!/usr/bin/env python3
"""Show that threads share a list while forked processes have separate memory."""
import os
import threading

def main():
    values=[0]
    def change_in_thread():
        values[0]=10
    t=threading.Thread(target=change_in_thread)
    t.start(); t.join()
    print(f"After thread changed list: {values}",flush=True)
    pid=os.fork()
    if pid==0:
        values[0]=99
        print(f"Inside child process: {values}",flush=True)
        os._exit(0)
    os.waitpid(pid,0)
    print(f"In parent after child changed its copy: {values}")
if __name__=="__main__": main()
