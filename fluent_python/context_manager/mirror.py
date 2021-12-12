"""
@author: magician
@file:   mirror.py
@date:   2021/12/12
"""
import sys


class LookingGlass:
    """
    LookingGlass
    """

    def __enter__(self):
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write

        return 'JABBERWOCKY'

    def reverse_write(self, text):
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero!')
            return True
