"""
    @author: magician
    @date: 2019/12/19
    @file: rm_element.py
"""


def remove_element(nums, val: int) -> int:
    """
    remove_element
    :param nums:
    :param val:
    :return:
    """
    num_list = []

    for i in nums:
        if i != val:
            num_list.append(i)
    print(num_list)

    return len(num_list)


if __name__ == '__main__':
    assert remove_element([3, 2, 2, 3], 3) == 2
