"""
@author: magician
@file:   abc_demo.py
@date:   2020/1/13
"""
from collections import Sequence


class FrequencyList(list):
    """
    FrequencyList
    """
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1

        return counts


class BinaryNode(object):
    """
    BinaryNode
    """
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class IndexableNode(BinaryNode):
    """
    IndexableNode
    """
    def _search(self, count, index):
        # pass
        return (count, index)

    def __getitem__(self, index):
        found, _ = self._search(0, index)

        if not found:
            raise IndexError('Index of range')

        return found.value


class SequenceNode(IndexableNode):
    """
    SequenceNode
    """
    def __len__(self):
        _, count = self._search(0, None)

        return count


class BadType(Sequence):
    """
    BadType
    """
    pass


class BetterNode(SequenceNode, Sequence):
    """
    BetterNode
    """
    pass


if __name__ == '__main__':
    foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
    print('Length is', len(foo))
    foo.pop()
    print('After pop:', repr(foo))
    print('Frequency:', foo.frequency())

    bar = [1, 2, 3]
    print(bar[0])
    print(bar.__getitem__(0))

    tree = IndexableNode(
        10,
        left=IndexableNode(
            5,
            left=IndexableNode(2),
            right=IndexableNode(
                6, IndexableNode(7))),
        right=IndexableNode(
            15, left=IndexableNode(11)))
    # print('LRR =', tree.left.right.right.value)
    # print('Index 0 =', tree[0])
    # print('Index 1 =', tree[1])
    # print('11 in the tree?', 11 in tree)
    # print('17 in the tree?', 17 in tree)
    # print('Tree is', list(tree))
    try:
        len(tree)
    except Exception as e:
        print(e)

    tree = SequenceNode(
        10,
        left=SequenceNode(
            5,
            left=SequenceNode(2),
            right=SequenceNode(
                6, SequenceNode(7))),
        right=SequenceNode(
            15, left=SequenceNode(11)))

    try:
        print('Tree has %d nodes' % len(tree))
    except Exception as e:
        print(e)

    try:
        foo = BadType()
    except Exception as e:
        print(e)

    print('Index of 7 is', tree.index(7))
    print('Count of 10 is', tree.count(7))
