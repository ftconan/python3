"""
    @author: magician
    @date: 2019/12/26
    @file: digit_demo.py
"""


def add_digits(num: int) -> int:
    while True:
        total = 0
        num_list = list(str(num))

        for i in num_list:
            total += int(i)
        if 0 <= total <= 9:
            break
        else:
            num = total

    return total


if __name__ == '__main__':
    assert add_digits(38) == 2
