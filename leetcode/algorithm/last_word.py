"""
    @author: magician
    @date: 2019/12/19
    @file: last_word.py
"""


def length_of_last_word(s):
    """
    length_of_last_word
    :param s:
    :return:
    """
    return len(s.strip().split(' ')[-1]) if s else 0


if __name__ == '__main__':
    assert length_of_last_word("Hello World") == 5
    assert length_of_last_word("a ") == 1
