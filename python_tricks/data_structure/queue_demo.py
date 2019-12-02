"""
    @author: magician
    @date: 2019/12/2
    @file: queue_demo.py
"""
from collections import deque
from queue import Queue
from multiprocessing import Queue as MQueue

if __name__ == '__main__':
    # list — Terribly Sloooow Queues
    q = list()
    q.append('eat')
    q.append('sleep')
    q.append('code')
    print(q)
    # Careful: This is slow!
    q.pop(0)
    print(q)

    # collections.deque – Fast & Robust Queues
    q = deque()
    q.append('eat')
    q.append('sleep')
    q.append('code')
    print(q)

    q.popleft()
    print(q)
    q.popleft()
    print(q)
    q.popleft()
    print(q)
    try:
        q.popleft()
    except Exception as e:
        print(e)

    # queue.Queue – Locking Semantics for Parallel Computing
    q = Queue()
    q.put('eat')
    q.put('sleep')
    q.put('code')
    print(q)

    print(q.get())
    print(q.get())
    print(q.get())
    try:
        print(q.get_nowait())
    except Exception as e:
        print(e)
    try:
        print(q.get())
    except Exception as e:
        print(e)

    # multiprocessing.Queue – Shared Job Queues
    q = MQueue()
    q.put('eat')
    q.put('sleep')
    q.put('code')
    print(q)

    print(q.get())
    print(q.get())
    print(q.get())
    print(q.get())
