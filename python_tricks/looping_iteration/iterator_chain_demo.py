"""
    @author: magician
    @date: 2019/12/6
    @file: iterator_chain_demo.py
"""


def integers():
    """
    integers
    :return:
    """
    return range(8)


def squared(seq):
    """
    squared
    :param seq:
    :return:
    """
    yield (i * i for i in seq)


def negated(seq):
    """
    negated
    :param seq:
    :return:
    """
    yield (-i for i in seq)


if __name__ == '__main__':
    # chain = integers()
    # print(list(chain))
    # new_chain = squared(chain)
    # print(list(new_chain))
    print(list(negated(list(squared(list(integers()))))))

    integers = range(8)
    squared = (i * i for i in integers)
    negated = (-i for i in squared)
    print(negated)
    print(list(negated))
