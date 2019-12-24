"""
    @author: magician
    @date: 2019/12/24
    @file: happy_number.py
"""
MAX_COUNT = 100


def is_happy(n: int) -> bool:
    """
    is_happy
    :param n:
    :return:
    """
    global happy_flag
    happy_flag = False
    total, counter = n, 0

    while True:
        num_list, total= list(str(total)), 0
        for i in num_list:
            total += pow(int(i), 2)

        counter += 1
        if total == 1 or counter == MAX_COUNT:
            if total == 1:
                happy_flag = True
            break

    return happy_flag


if __name__ == '__main__':
    assert is_happy(19) is True
    assert is_happy(20) is False
