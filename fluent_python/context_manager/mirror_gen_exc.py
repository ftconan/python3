"""
@author: magician
@file:   mirror_gen_exc.py
@date:   2021/12/12
"""
import contextlib
import sys


@contextlib.contextmanager
def looking_glass():
    """
    looking_glass
    @return:
    """
    original_write = sys.stdout.write

    def reverse_write(text):
        """

        @param text:
        @return:
        """
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    msg = ''
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)
