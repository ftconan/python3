# coding=utf-8

"""
@author: conan
@date: 2018/6/24
"""
import random


def number_game():
    """
    数字游戏
    :return:
    """
    print('*'*8 + '开始数字游戏' + '*'*8)

    #  游戏竞猜循环
    count = 0

    secret = random.randint(0, 10)
    while True:
        # 计数器，三次都没猜中，跳出循环
        if count != 3:
            number = input('请输入一个我喜欢的数字,只有三次机会哦!:\n')
            try:
                number = int(number)
                if number == secret:
                    print('恭喜您猜中啦!')
                    break
                else:
                    if number > secret:
                        print('猜错咯!数字大了一点点!')
                    else:
                        print('猜错咯!数字小了一丢丢!')
            except Exception as e:
                print(e)
                print('请输入一个正确的数字!')
        else:
            print('三次都没猜中哦，GAME OVER!')
            break

        count += 1

    print('游戏结束咯!')


if __name__ == '__main__':
    number_game()
