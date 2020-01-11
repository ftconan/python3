"""
    @author: magician
    @date: 2020/01/10
    @file: miss_num.py
"""


def missing_number(nums) -> int:
    """
    missing number
    @param nums:
    @return:
    """
    nums.sort()
    miss_num = None

    if nums:
        num1, num2 = min(nums), max(nums)
        miss_num = list(set(range(num1, num2 + 1)) - set(nums))
        if miss_num:
            miss_num = miss_num[0]
        else:
            if len(nums) == 1:
                if nums[0] > 0:
                    miss_num = nums[0] - 1
                else:
                    miss_num = 1
            else:
                if nums[0] >= 1:
                    miss_num = nums[0] - 1
                else:
                    miss_num = nums[-1] + 1

    return miss_num


if __name__ == '__main__':
    assert missing_number([3, 0, 1]) == 2
    assert missing_number([0]) == 1
    assert missing_number([1]) == 0
    assert missing_number([0, 1]) == 2
    assert missing_number([1, 2]) == 0
