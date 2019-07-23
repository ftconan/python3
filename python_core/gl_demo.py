"""
@file: gl_demo.py
@author: magician
@date: 2019/7/23
"""
import functools
import os
import sys
import gc
import objgraph
import psutil


def print_memory():
    """
    print_memory
    :return:
    """
    pid = os.getpid()
    p = psutil.Process(pid)

    info = p.memory_full_info()
    memory = info.uss / 1024. / 1024
    print('memory used: {} MB'.format(memory))

    return memory


def show_memory_info(func1):
    """
    show_memory_info
    :param: func1
    :return:
    """
    @functools.wraps(func1)
    def wrapper():
        """
        wrapper
        :return:
        """
        memory1 = print_memory()
        func1()
        memory2 = print_memory()
        print('memory used all: {} MB'.format(memory2 - memory1))

    return wrapper


@show_memory_info
def func():
    """
    func
    :return:
    """
    return [i for i in range(10000000)]


def count_a():
    """
    count_a
    :return:
    """
    a = []
    print(sys.getrefcount(a))

    b = a
    print(sys.getrefcount(a))

    c = b
    d = b
    e = c
    f = e
    g = d
    print(sys.getrefcount(a))


@show_memory_info
def manual_gc():
    """
    manual_gc
    :return:
    """
    a = [i for i in range(10000000)]
    del a
    gc.collect()


@show_memory_info
def circular_reference():
    """
    circular reference
    :return:
    """
    a = [i for i in range(10000000)]
    b = [i for i in range(10000000)]
    a.append(b)
    b.append(a)


def show_graph():
    """
    show_graph
    :return:
    """
    a = [1, 2, 3]
    b = [4, 5, 6]

    a.append(b)
    b.append(a)

    objgraph.show_refs([a])
    objgraph.show_backrefs([a])


if __name__ == '__main__':
    func()

    count_a()

    manual_gc()

    circular_reference()
    gc.collect()
    print_memory()

    show_graph()
