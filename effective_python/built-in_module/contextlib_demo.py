"""
@author: magician
@file:   contextlib_demo.py
@date:   2020/8/10
"""
import logging
from contextlib import contextmanager
from threading import Lock


def my_function():
    logging.debug('Some debug data')
    logging.debug('Error log here')
    logging.debug('More debug here')


@contextmanager
def debug_logging(level):
    """
    debug_logging
    @param level:
    @return:
    """
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)


@contextmanager
def log_level(level, name):
    """
    log_level
    @param level:
    @param name:
    @return:
    """
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)


if __name__ == '__main__':
    lock = Lock()
    with lock:
        print('Lock is held')

    lock.acquire()
    try:
        print('Lock is held')
    finally:
        lock.release()

    my_function()

    with debug_logging(logging.DEBUG):
        print('Inside:')
        my_function()

    with log_level(logging.DEBUG, 'my-log') as logger:
        logger.debug('This is my message!')
        logging.debug('This will not print')
        logger = logging.getLogger('my-log')
        logger.debug('Debug will not print')
        logger.error('Error will print')
