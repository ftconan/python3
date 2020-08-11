"""
@author: magician
@file:   decimal_demo.py
@date:   2020/8/11
"""
import decimal

if __name__ == '__main__':
    rate = 1.45
    seconds = 3 * 60 + 42
    cost = rate * seconds / 60
    print(cost)
    print(round(cost, 2))

    rate = 0.05
    seconds = 5
    cost = rate * seconds / 60
    print(cost)

    rate = decimal.Decimal('1.45')
    seconds = decimal.Decimal('222')
    cost = rate * seconds / decimal.Decimal('60')
    print(cost)
    rounded = cost.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_UP)
    print(rounded)

    rate = decimal.Decimal('0.05')
    seconds = decimal.Decimal('5')
    cost = rate * seconds / decimal.Decimal('60')
    print(cost)
    rounded = cost.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_UP)
    print(rounded)
