"""
    @author: magician
    @date: 2019/11/9
    @file: assert_demo.py
"""


def apply_discount(product, discount):
    """
    apply discount
    :param product:
    :param discount:
    :return:
    """
    price = int(product['price'] * (1.0 - discount))
    assert 0 <= price <= product['price']
    print(price)

    return price


class AuthError(object):
    """
    AuthError
    """
    def __init__(self, error):
        self.error = error


def delete_product(product_id, user, store=None):
    """
    delete product
    :param product_id:
    :param user:
    :param store:
    :return:
    """
    if not user.is_admin():
        raise AuthError('Must be admin to delete')
    if not store.has_product(product_id):
        raise ValueError('Unknown product id')

    store.get_product(product_id).delete()

    return True


if __name__ == '__main__':
    shoes = {'name': 'Fancy Shoes', 'price': 14900}
    apply_discount(shoes, 0.25)
    apply_discount(shoes, 2.0)
    apply_discount(prod, 2.0)
    #  SyntaxWarning: assertion is always true
    assert(1 == 2, 'This should fail')
