"""
    @author: magician
    @date: 2019/12/20
    @file: single_num.py
"""
import collections


def single_number(nums) -> int:
    num_list = [k for k, v in collections.Counter(nums).items() if v == 1]

    return num_list[0]


if __name__ == '__main__':
    assert single_number([2,2,1]) == 1
