"""
@author: magician
@file:   sentence_iter.py
@date:   2020/12/14
"""
import re
import reprlib

RE_WORD = re.compile(r'\w+')


class SentenceIterator:
    """
    SentenceIterator
    """

    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1

        return word

    def __iter__(self):
        return self


class Sentence:
    """
    Sentence
    """

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        return SentenceIterator(self.words)
