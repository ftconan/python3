"""
    @author: magician
    @date: 2019/12/13
    @file: generator_demo.py
"""
from itertools import islice


def index_words(text):
    """
    index_words
    :param text:
    :return:
    """
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)

    return result


def index_words_iter(text):
    """
    index_words_iter
    :param text:
    :return:
    """
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1


def index_file(handle):
    """
    index_file
    :param handle:
    :return:
    """
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset


if __name__ == '__main__':
    address = 'Four score and seven years ago...'
    result = index_words(address)
    print(result[:3])

    result = list(index_words_iter(address))
    print(result[:3])

    with open('/home/magician/Project/python3/data/address.txt', 'r') as f:
        it = index_file(f)
        result = islice(it, 0, 3)
        print(list(result))
