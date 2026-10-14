#!/usr/bin/env python3
"""Demonstrate that processes do not share ordinary Python lists, then share data explicitly."""
from multiprocessing import Process, shared_memory
from array import array

def change_regular_list(values):
    values[0] = -100

def change_shared_memory(name, length):
    shm = shared_memory.SharedMemory(name=name)
    try:
        numbers = array("q")
        numbers.frombytes(shm.buf[:length * numbers.itemsize])
        numbers[0] = -100
        shm.buf[:length * numbers.itemsize] = numbers.tobytes()
    finally:
        shm.close()

def main():
    ordinary = [10, 20, 30]
    process = Process(target=change_regular_list, args=(ordinary,))
    process.start()
    process.join()
    print("Ordinary list in parent:", ordinary)
    print("The parent's list remains unchanged because a process has its own address space.")

    original = array("q", [10, 20, 30])
    shm = shared_memory.SharedMemory(create=True, size=len(original) * original.itemsize)
    try:
        shm.buf[:len(original) * original.itemsize] = original.tobytes()
        process = Process(target=change_shared_memory, args=(shm.name, len(original)))
        process.start()
        process.join()
        shared_result = array("q")
        shared_result.frombytes(shm.buf[:len(original) * original.itemsize])
        print("Shared-memory array in parent:", list(shared_result))
        print("The first value changed because both processes access the same shared-memory block.")
    finally:
        shm.close()
        shm.unlink()

if __name__ == "__main__":
    main()
