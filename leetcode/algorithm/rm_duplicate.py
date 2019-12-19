"""
    @author: magician
    @date: 2019/12/19
    @file: rm_duplicate.py
"""
from _ast import List


def remove_duplicates(nums) -> int:
    """
    remove_duplicates
    :param nums:
    :return:
    """
    # print(list(set(nums)))

    return len(set(nums))


if __name__ == '__main__':
    assert remove_duplicates([1, 1, 2]) == 2
