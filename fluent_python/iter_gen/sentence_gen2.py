"""
@author: magician
@file:   sentence_gen2.py
@date:   2020/12/14
"""
import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:
    """
    Sentence
    """

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):
            yield match.group()
