# coding=utf-8

"""
@author: conan
@date: 2018/6/24
"""


def number_game():
    """
    数字游戏
    :return:
    """
    print('*'*8 + '开始数字游戏' + '*'*8)

    #  游戏竞猜循环
    while True:
        number = input('请输入一个我喜欢的数字:\n')
        try:
            number = int(number)
            if number == 8:
                print('恭喜您猜中啦!')
                break
            else:
                print('猜错咯，继续努力!')
        except Exception as e:
            print(e)
            print('请输入一个正确的数字!')

    print('游戏结束咯!')


if __name__ == '__main__':
    number_game()
