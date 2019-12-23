"""
    @author: magician
    @date: 2019/12/23
    @file: most_element.py
"""
import collections


def majority_element(nums) -> int:
    """
    majority_element
    :param nums:
    :return:
    """
    counter = collections.Counter(nums)
    num = counter.most_common(1)

    return num[0][0] if nums else 0


if __name__ == '__main__':
    assert majority_element([3, 2, 3]) == 3
