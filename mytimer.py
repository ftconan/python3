# coding=utf-8

"""
@author: conan
@date: 2018/7/15
"""
import time


class MyTimer:
    """
    MyTimer
    """
    def __init__(self):
        self.begin = 0
        self.end = 0
        self.cal_time = 0
        self.prompt = '未开始计时'

    def __str__(self):
        return self.prompt

    __repr__ = __str__

    def __add__(self, other):
        add_time = '总共计时...' + str(int(self.cal_time) + int(other.cal_time)) + 's'
        return add_time

    def start(self):
        """
        start
        :return:
        """
        self.begin = int(round(time.time()))
        self.prompt = '请点击stop停止计时'
        print('开始计时...')

    def stop(self):
        """
        stop
        :return:
        """
        if self.begin:
            self.end = int(round(time.time()))
            self.cal_time = self.end - self.begin
            self.prompt = '总共运行...' + str(self.cal_time) + 's'
            print('停止计时')
        else:
            print('请点击start开始计时')

        # 清空数据
        self.begin = 0
        self.end = 0


if __name__ == '__main__':
    t1 = MyTimer()
    t1.stop()
    t1.start()
    time.sleep(2)
    t1.stop()
    print(t1)

    t2 = MyTimer()
    t2.stop()
    t2.start()
    time.sleep(4)
    t2.stop()
    print(t2)

    print(t1 + t2)
