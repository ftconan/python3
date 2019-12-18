"""
    @author: magician
    @date: 2019/12/18
    @file: sum_of_two.py
"""


def two_sum(nums, target):
    """
    two sum
    :param nums:
    :param target:
    :return:
    """
    i, index_list = 1, []

    for index1, value1 in enumerate(nums):
        new_nums = nums[index1 + 1:]
        for index2, value2 in enumerate(new_nums):
            if value1 + value2 == target:
                index_list.append(index1)
                index_list.append(index2 + i)
        i += 1

    return list(set(index_list))


if __name__ == '__main__':
    result1 = two_sum([3, 2, 4], 6)
    print(result1)

    result2 = two_sum([3, 3], 6)
    print(result2)
