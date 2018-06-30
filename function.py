# coding=utf-8

"""
@author: conan
@date: 2018/6/29
"""


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

