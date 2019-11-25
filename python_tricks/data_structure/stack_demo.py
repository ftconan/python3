"""
    @author: magician
    @date: 2019/11/25
    @file: stack_demo.py
"""
from collections import deque
from queue import LifoQueue

if __name__ == '__main__':
    s = list()
    s.append('eat')
    s.append('sleep')
    s.append('code')
    print(s)
    s.pop()
    s.pop()
    s.pop()
    try:
        s.pop()
    except Exception as e:
        print(e)

    # collections.deque – Fast & Robust Stacks
    s = deque()
    s.append('eat')
    s.append('sleep')
    s.append('code')
    print(s)
    s.pop()
    s.pop()
    s.pop()
    try:
        s.pop()
    except Exception as e:
        print(e)

    # queue.LifoQueue – Locking Semantics for Parallel Computing
    s = LifoQueue()
    s.put('eat')
    s.put('sleep')
    s.put('code')
    print(s)
    s.get()
    s.get()
    s.get()
    try:
     s.get_nowait()
    except Exception as e:
        print(e)
    try:
        s.get()
    except Exception as e:
        print(e)

    # Comparing Stack Implementations in Python
    pass
