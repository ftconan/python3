"""
    @author: magician
    @date: 2019/12/18
    @file: max_prefix.py
"""
from typing import List


def longest_common_prefix(strs: List[str]) -> str:
    """
    longest_common_prefix
    :param strs:
    :return:
    """
    flag = False
    prefix_str = ''

    if strs:
        first_str = strs[0]

        for i in range(len(first_str)):
            prefix_str = first_str[:i + 1]
            for item in strs:
                if not (prefix_str in item and prefix_str == item[:i + 1]):
                    flag = True
                    break
            if flag:
                prefix_str = first_str[:i]
                break

    return prefix_str


if __name__ == '__main__':
    assert longest_common_prefix(["flower","flow","flight"]) == "fl"
    assert longest_common_prefix(["c","acc","ccc"]) == ""
