"""
    @author: magician
    @date: 2019/11/9
    @file: assert_demo.py
"""


def apply_discount(product, discount):
    """
    appy discount
    :param product:
    :param discount:
    :return:
    """
    price = int(product['price'] * (1.0 - discount))
    assert 0 <= price <= product['price']
    print(price)

    return price


if __name__ == '__main__':
    shoes = {'name': 'Fancy Shoes', 'price': 14900}
    apply_discount(shoes, 0.25)
    apply_discount(shoes, 2.0)
