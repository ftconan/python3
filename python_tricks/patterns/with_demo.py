"""
    @author: magician
    @date: 2019/11/15
    @file: with_demo.py
"""
import os
import threading
from contextlib import contextmanager
from data import DATA_DIR

FILE_PATH = os.path.join(DATA_DIR, 'hello.txt')


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
    my_file = None
    try:
        my_file = open(name, 'w')
        yield my_file
    finally:
        my_file.close()


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
    with open(FILE_PATH, 'w') as f:
        f.write('hello world')

    f = open(FILE_PATH, 'w')
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
    with ManagedFile(FILE_PATH) as f:
        f.write('hello, world!')
        f.write('bye now')

    # managed_file decoration
    with managed_file(FILE_PATH) as f:
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
