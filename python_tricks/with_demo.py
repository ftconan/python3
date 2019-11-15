"""
    @author: magician
    @date: 2019/11/15
    @file: comma_demo.py
"""
import threading


class ManagedFile:
    """
    ManagedFile
    """
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.file = open(self.name, 'w')

        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()


if __name__ == '__main__':
    with open('../data/hello.txt', 'w') as f:
        f.write('hello world')

    f = open('hello.txt', 'w')
    try:
        f.write('hello, world')
    finally:
        f.close()

    some_lock = threading.Lock()
    # Harmful:
    some_lock.acquire()
    try:
        pass
    finally:
        some_lock.release()

    # Better
    with some_lock:
        pass

