"""
    @author: magician
    @date: 2019/12/2
    @file: priority_queue_demo.py
"""
import heapq
from queue import PriorityQueue

if __name__ == '__main__':
    # list — Terribly Sloooow Queues
    q = list()
    q.append((2, 'code'))
    q.append((1, 'eat'))
    q.append((3, 'sleep'))
    # NOTE: Remember to re-sort every time
    # a new element is inserted, or use
    # bisect.insort()
    q.sort(reverse=True)

    while q:
        next_item = q.pop()
        print(next_item)

    # heapq – List-Based Binary Heaps
    q = []
    heapq.heappush(q, (2, 'code'))
    heapq.heappush(q, (1, 'eat'))
    heapq.heappush(q, (3, 'sleep'))

    while q:
        next_item = heapq.heappop(q)
        print(next_item)

    # queue.PriorityQueue – Beautiful Priority Queues
    q = PriorityQueue()
    q.put((2, 'code'))
    q.put((1, 'eat'))
    q.put((3, 'sleep'))

    while not q.empty():
        next_item = q.get()
        print(next_item)
