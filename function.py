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


if __name__ == '__main__':
    print(number_game.__doc__)
    print(test_params('China', 'I love you!', 'hello ', '1', '2', '3'))

