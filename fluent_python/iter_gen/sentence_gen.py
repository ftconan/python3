"""
@author: magician
@file:   sentence_gen.py
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
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:
            yield word


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said,')
    print(s.__iter__())
