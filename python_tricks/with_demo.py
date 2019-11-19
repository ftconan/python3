"""
    @author: magician
    @date: 2019/11/15
    @file: comma_demo.py
"""
import threading
from contextlib import contextmanager


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


@contextmanager
def managed_file(name):
    """
    managed_file
    :param name:
    :return:
    """
    try:
        f = open(name, 'w')
        yield f
    finally:
        f.close()


class Indenter:
    """
    Indenter
    """
    def __init__(self):
        self.level = 0

    def __enter__(self):
        self.level += 1

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.level -= 1

    def print(self, text):
        print('    ' * self.level + text)




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

    # ManagedFile Class
    with ManagedFile('hello.txt') as f:
        f.write('hello, world!')
        f.write('bye now')

    # managed_file decoration
    with managed_file('hello.txt') as f:
        f.write('hello, world!')
        f.write('bye now')

    # indentation
    with Indenter() as indent:
        indent.print('hi!')
        with indent:
            indent.print('hello')
            with indent:
                indent.print('bojour')
        indent.print('hey')
