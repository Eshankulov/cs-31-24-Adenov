#!/usr/bin/env python3
"""Dining philosophers with unsafe, ordered-lock and room-limiter strategies."""
import argparse, threading

def run(strategy, rounds):
    n=5; forks=[threading.Lock() for _ in range(n)]; meals=[0]*n
    room=threading.Semaphore(n-1) if strategy=="room" else None
    def worker(i):
        for _ in range(rounds):
            if room: room.acquire()
            left,right=forks[i],forks[(i+1)%n]
            first,second=left,right
            if strategy=="ordered" and (i+1)%n < i: first,second=right,left
            first.acquire(); second.acquire()
            meals[i]+=1
            second.release(); first.release()
            if room: room.release()
    threads=[threading.Thread(target=worker,args=(i,),daemon=(strategy=="deadlock")) for i in range(n)]
    for t in threads:t.start()
    if strategy=="deadlock":
        for t in threads:t.join(timeout=1)
        print("unsafe strategy completed:",all(not t.is_alive() for t in threads),"(deadlock possible, not guaranteed)")
    else:
        for t in threads:t.join()
        print(f"strategy={strategy}; meals per philosopher={meals}; total={sum(meals)}")
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--strategy",choices=["deadlock","ordered","room"],default="ordered"); p.add_argument("--rounds",type=int,default=100); a=p.parse_args(); run(a.strategy,a.rounds)
