"""
    @author: magician
    @date: 2019/12/13
    @file: for_demo.py
"""


def coprime(a, b):
    """
    coprime
    :param a:
    :param b:
    :return:
    """
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return False

    return True


def coprime2(a, b):
    """
    coprime2
    :param a:
    :param b:
    :return:
    """
    is_coprime = True
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_coprime = False
            break

    return is_coprime


if __name__ == '__main__':
    for i in range(3):
        print('Loop {0}'.format(i))
    else:
        print('Else block!')

    for i in range(3):
        print('Loop {0}'.format(i))
        if i == 1:
            break
    else:
        print('Else block!')

    for x in []:
        print('Never runs')
    else:
        print('For Else block!')

    while False:
        print('Never runs')
    else:
        print('While Else block!')

    a, b = 4, 9
    for i in range(2, min(a, b) + 1):
        print('Testing', i)
        if a % i == 0 and b % i == 0:
            print('Not coprime')
            break
    else:
        print('Coprime')

    print(coprime(a, b))
    print(coprime2(a, b))
