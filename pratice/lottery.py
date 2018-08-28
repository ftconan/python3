# coding=utf-8

"""
@author: conan
@date: 2018/8/26
"""

# def calc_(proportion):
#     """
#     n阶乘
#     :param n:
#     :return:
#     """
#     return 1 if n < 2 else n * factorial(n - 1)
from collections import Counter

if __name__ == '__main__':
    # property_list = [7.50, 3.70, 3.00, 3.85, 6.50, 12.00, 21.00, 31.00]
    # property_list = [7.00, 3.40, 2.97, 3.95, 7.00, 13.00, 25.00, 38.00]
    # property_list = [60.00, 17.00, 8.50, 5.30, 4.50, 4.50, 5.30, 3.35]
    # total_score_property = sum(property_list)
    # print('total_score_property', total_score_property)
    # print('win_rate', 'lose_rate', sum(property_list[2:5]) / total_score_property,
    #       1 - sum(property_list[2:5]) / total_score_property)

    # point_list = [6, 17, 14, 11, 9, 13, 8, 15, 13, 9, 10, 7, 9, 7, 8, 14, 9, 17, 13, 9, 6, 16, 12, 16, 14, 16, 8, 11,
    #               6, 10, 11, 9, 7, 13, 11, 7, 15, 9, 8, 13, 7, 6, 14, 10, 9, 11, 10, 14, 8, 13, 9, 14, 8, 8, 12, 10,
    #               4, 9, 9, 8, 9, 12, 9, 11, 11, 9]
    point_list = [8, 11, 16, 8, 13, 10, 15, 10, 9, 12, 9, 13, 8, 6, 13, 6, 16, 11]
    print('27 point length', len(point_list))
    print('point number', set(point_list))
    print('point length', len(set(point_list)))

    # 统计数字出现次数
    count = Counter(point_list)
    print(count.most_common(len(set(point_list))))
    # print(sorted(count. keys=count.values()))
