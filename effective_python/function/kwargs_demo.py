"""
    @author: magician
    @date: 2019/12/18
    @file: kwargs_demo.py
"""


def remainder(number, divisor):
    """
    remainder
    :param number:
    :param divisor:
    :return:
    """
    return number % divisor


def flow_rate(weight_diff, time_diff, period=1, units_per_kg=1):
    """
    flow_rate
    :param weight_diff:
    :param time_diff:
    :param period:
    :param units_per_kg:
    :return:
    """
    return ((weight_diff * units_per_kg) / time_diff) * period


if __name__ == '__main__':
    assert remainder(20, 7) == 6
    print(remainder(20, 7))
    print(remainder(20, divisor=7))
    print(remainder(number=20, divisor=7))
    print(remainder(divisor=20, number=7))
    # try:
    #     print(number=20, 7)
    # except Exception as e:
    #     print(e)
    try:
        print(20, number=7)
    except Exception as e:
        print(e)

    weight_diff, time_diff = 0.5, 3
    flow = flow_rate(weight_diff, time_diff)
    print('%.3f kg per second' % flow)

    flow_per_second = flow_rate(weight_diff, time_diff, 1)
    print(flow_per_second)
    flow_per_hour = flow_rate(weight_diff, time_diff, 3600)
    print(flow_per_hour)

    pounds_per_hour = flow_rate(weight_diff, time_diff, period=3600, units_per_kg=2.2)
    print(pounds_per_hour)
