"""
    @author: magician
    @date: 2019/12/24
    @file: rotate_array.py
"""


def rotate(nums, k: int) -> None:
    """
    Do not return anything, modify nums in-place instead.
    """
    # nums = nums[k + 1:] + nums[:k + 1]

    for i in range(k):
        nums.insert(0, nums[-1])
        nums.pop()

    return nums


if __name__ == '__main__':
    assert rotate([1,2,3,4,5,6,7], 3) == [5,6,7,1,2,3,4]

