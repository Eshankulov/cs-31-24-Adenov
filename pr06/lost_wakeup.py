#!/usr/bin/env python3
"""Illustrate the unsafe if-before-wait pattern; do not use in production."""
import threading
cv=threading.Condition()
items=[]
def consumer():
    with cv:
        if not items:  # BUG: must be while, not if
            print("consumer: queue empty; waiting")
            cv.wait()
        # Incorrectly assumes notification guarantees an item.
        if not items:
            print("BUG reproduced: woke up but queue is still empty")
        else:
            print("consumed",items.pop(0))
def main():
    with cv:
        cv.notify_all()  # notification before consumer waits is not remembered
    t=threading.Thread(target=consumer)
    t.start(); t.join(timeout=1)
    if t.is_alive():
        print("consumer is still waiting: notification was lost")
        with cv:
            items.append("late item")
            cv.notify_all()
        t.join()
if __name__=="__main__": main()
