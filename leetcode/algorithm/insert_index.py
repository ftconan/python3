"""
    @author: magician
    @date: 2019/12/20
    @file: insert_index.py
"""


def search_insert(nums, target: int) -> int:
    """
    search_insert
    :param nums:
    :param target:
    :return:
    """
    index = 0

    if target in nums:
        index = nums.index(target)
    else:
        if target < min(nums):
            index = 0
        elif target > max(nums):
            index = len(nums)
        else:
            for num in nums:
                index = nums.index(num)
                if target < num:
                    break

    return index


if __name__ == '__main__':
    assert search_insert([1, 3, 5, 6], 5) == 2
    assert search_insert([1, 3, 5, 6], 0) == 0
    assert search_insert([1, 3, 5, 6], 7) == 4
