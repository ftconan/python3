"""
    @author: magician
    @date: 2019/12/10
    @file: str_demo.py
"""
import os


def to_str(bytes_or_str):
    """
    to_str(python2, python3)
    :param bytes_or_str:
    :return:
    """
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str

    return value


def to_bytes(bytes_or_str):
    """
    to_bytes(python3)
    :param bytes_or_str:
    :return:
    """
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str

    return value


def to_unicode(unicode_or_str):
    """
    to_unicode(python2)
    :param unicode_or_str:
    :return:
    """
    if isinstance(unicode_or_str, str):
        value = unicode_or_str.decode('utf-8')
    else:
        value = unicode_or_str

    return value


if __name__ == '__main__':
    with open('../../data/test_str.txt', 'wb+') as f:
        f.write(os.urandom(10))
