"""
@author: magician
@file:   collection_demo.py
@date:   2020/8/11
"""
import bisect
import random
from collections import deque, OrderedDict, defaultdict
from heapq import heappush, heappop, nsmallest

if __name__ == '__main__':
    # deque
    fifo = deque()
    fifo.append(1)  # Producer
    x = fifo.popleft()  # Consumer

    a = dict()
    a['foo'] = 1
    a['bar'] = 2

    # Randomly populate 'b' to cause hash conflicts
    # while True:
    z = random.randint(99, 101)
    b = dict()
    for i in range(z):
        b[i] = i
    b['foo'] = 1
    b['bar'] = 2
    for i in range(z):
        del b[i]
        # if str(b) != str(a):
        #     break

    print(a)
    print(b)
    print('Equal?', a == b)

    # OrderedDict
    a = OrderedDict()
    a['foo'] = 1
    a['bar'] = 2
    b = OrderedDict()
    b['foo'] = 'red'
    b['bar'] = 'blue'

    for value1, value2 in zip(a.values(), b.values()):
        print(value1, value2)

    # defaultdict
    stats = defaultdict(int)
    stats['my_counter'] += 1

    # heap
    a = []
    heappush(a, 5)
    heappush(a, 3)
    heappush(a, 7)
    heappush(a, 4)
    # print(heappop(a), heappop(a), heappop(a), heappop(a))
    assert a[0] == nsmallest(1, a)[0] == 3
    print('Before:', a)
    a.sort()
    print('After:', a)

    # bisect
    x = list(range(10**6))
    i = x.index(991234)
    print(i)
    i1 = bisect.bisect_left(x, 991234)
    print(i1)
