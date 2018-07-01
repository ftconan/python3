# coding=utf-8

"""
@author: conan
@date: 2018/6/29
"""
from functools import reduce


def number_game():
    """
    数字游戏
    :return:
    """
    print('*'*8 + '开始数字游戏' + '*'*8)


def test_params(name, word, title='Really?', *params):
    """
    参数测试
    1. 必传参数
    2. 默认参数
    3. 关键字参数
    4. 可变参数
    :param name:
    :param word:
    :param title:
    :param *params:
    :return:
    """
    return name + ',' + word + title + '\n' + str(len(params))


def update_global_variable():
    """
    修改全集变量(global关键字)
    :return:
    """
    global count
    count = 10
    return count


def outer_function(x):
    """
    闭包
    函数内部定义函数，并且应用外部函数变量，同时返回该内部函数的函数称为闭包
    :param x:
    :return:
    """
    def inner_function(y):
        return x * y
    return inner_function


def test_nonlocal():
    """
    测试python3 新特性nonlocal
    :return:
    """
    x = 5

    def local_function():
        nonlocal x
        x *= x
        return x
    return local_function()


def factorial(n):
    """
    普通阶乘
    :param n:
    :return:
    """
    result = n
    for i in range(1, n):
        result *= i
    return result


def recursion_fac(n, result=1):
    """
    递归阶乘
    :param n:
    :param result:
    :return:
    """
    if n > 0:
        result *= n
        return recursion_fac(n-1, result)

    return result


def fac(n):
    """
    递归阶乘
    :param n:
    :return:
    """
    if n == 1:
        return 1
    else:
        return n * fac(n - 1)


def fab(n):
    """
    斐波那契数列
    :param n:
    :return:
    """
    if n < 0:
        return -1

    if n == 1 or n == 2:
        return 1
    else:
        return fab(n - 1) + fab(n-2)


def hanoi(n, x, y, z):
    """
    汉诺塔
    :param n: 盘子数量
    :param x: 1号针
    :param y: 2号针
    :param z: 3号针
    :return:
    """
    if n == 1:
        print(x, '--> ', z)
    else:
        # 1. 将前n-1个盘子从x移动到y
        hanoi(n-1, x, z, y)
        # 2. 将最底下最后一个盘子从x移动到z
        print(x, '--> ', z)
        # 3. 将前n-1个盘子从y移动到z
        hanoi(n-1, y, x, z)


if __name__ == '__main__':
    print(number_game.__doc__)
    print(test_params('China', 'I love you!', 'hello ', '1', '2', '3'))

    # 全局变量
    count = 5
    print('全局变量：', count)
    update_global_variable()
    print('修改全局变量：', count)

    print(outer_function(5)(8))
    print(test_nonlocal())

    # lambda 匿名函数
    line = lambda x: 2 * x + 1
    print(line(5))

    add_fuc = lambda x, y: x + y
    print(add_fuc(3, 4))

    # filter过滤器(过滤偶数)
    print(list(filter(lambda x: x % 2, range(10))))

    # map遍历
    print(list(map(lambda x: x * 2, range(10))))

    # reduce 迭代(python3 废除, 隐藏在functools中)
    print(reduce(lambda x, y: x + y, range(101)))

    # 阶乘
    print(factorial(10))
    print(recursion_fac(10))
    print(fac(10))

    # 斐波那契数列
    print('fabonacci:')
    print(fab(10))

    # 汉诺塔
    print('hanoi:')
    hanoi(5, 'X', 'Y', 'Z')
