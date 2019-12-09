"""
    @author: magician
    @date: 2019/12/9
    @file: bytecode_demo.py
"""
import dis


def greet(name):
    """
    greet
    :param name:
    :return:
    """
    return 'Hello, ' + name + '!'


if __name__ == '__main__':
    print(greet('Guido'))
    print(greet.__code__.co_code)
    print(greet.__code__.co_consts)
    print(greet.__code__.co_varnames)

    print(dis.dis(greet))
