"""
@author: magician
@file:   queue_demo.py
@date:   2020/8/10
"""
import time
from collections import deque
from queue import Queue
from threading import Lock, Thread


class MyQueue(object):
    """
    MyQueue
    """

    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()


class Worker(Thread):
    """
    Worker
    """

    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                time.sleep(0.01)  # No work to do
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


def download(args):
    pass


def resize(args):
    pass


def upload(args):
    pass


queue = Queue()


def consumer():
    print('Consumer waiting')
    queue.get()  # Runs after put() below
    print('Consumer done')


if __name__ == '__main__':
    download_queue = MyQueue()
    resize_queue = MyQueue()
    upload_queue = MyQueue()
    done_queue = MyQueue()

    threads = [
        Worker(download, download_queue, resize_queue),
        Worker(resize, download_queue, upload_queue),
        Worker(upload, upload_queue, done_queue),
    ]
    for thread in threads:
        thread.start()
    for _ in range(1000):
        download_queue.put(object())
    while len(done_queue.items) < 1000:
        time.sleep(1)
        break

    processed = len(done_queue.items)
    polled = len(done_queue.items)
    print('Processed', processed, 'items after polling', polled, 'times')

    thread = Thread(target=consumer)
    thread.start()
    print('Producer putting')
    queue.put(object())  # Runs before get() above
    thread.join()
    print('Producer done')
