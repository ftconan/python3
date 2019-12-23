"""
    @author: magician
    @date: 2019/12/23
    @file: merge_list.py
"""


def merge(nums1, m: int, nums2, n) -> None:
    """
    Do not return anything, modify nums1 in-place instead.
    """
    if len(nums1) >= m + n:
        for num in nums2:
            nums1[m] = num
            m += 1
        nums1.sort()

    return nums1


if __name__ == '__main__':
    assert merge([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3) == [1, 2, 2, 3, 5, 6]
