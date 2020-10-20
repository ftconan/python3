"""
@author: magician
@file:   patterns_demo.py
@date:   2020/10/20
"""
import collections
import inspect

Customer = collections.namedtuple('Customer', 'name fidelity')


class LineItem:
    """
    LineItem
    """

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:
    """
    Order
    """

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)

        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)

        return self.total() - discount

    def __repr__(self):
        return '<Order total: {:.2f} due: {:.2f}>'.format(self.total(), self.due())


def fidelity_promo(order):
    """
    为积分为1000或以上的顾客提供5%折扣
    @param order:
    @return:
    """
    return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0


def bulk_item_promo(order):
    """
    单个商品为20个或以上时提供10%折扣
    @param order:
    @return:
    """
    discount = 0

    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * 0.1

    return discount


def large_order_promo(order):
    """
    订单中的不同商品达到10个或以上时提供7%折扣
    @param order:
    @return:
    """
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * 0.07

    return 0


# promos = [fidelity_promo, bulk_item_promo, large_order_promo]
promos = [globals()[name] for name in globals() if name.endswith('_promo') and name != 'best_promo']


# promos = [func for name, func in inspect.getmembers(promotions, inspect.isfunction)]


def best_promo(order):
    """
    选择可用的最佳折扣
    @param order:
    @return:
    """
    return max(promo(order) for promo in promos)


class MacroCommand:
    """
    一个执行一组命令的命令
    """

    def __init__(self, commands):
        self.commands = list(commands)

    def __call__(self, *args, **kwargs):
        for command in self.commands:
            command()


if __name__ == '__main__':
    joe = Customer('John Doe', 0)
    ann = Customer('Ann Smith', 1100)
    cart = [
        LineItem('banana', 4, 0.5),
        LineItem('apple', 10, 1.5),
        LineItem('watermelon', 5, 5.0),
    ]
    print(Order(joe, cart, fidelity_promo))
    print(Order(ann, cart, fidelity_promo))

    banana_cart = [
        LineItem('banana', 30, 0.5),
        LineItem('apple', 10, 1.5),
    ]
    print(Order(joe, banana_cart, bulk_item_promo))

    long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
    print(Order(joe, long_order, large_order_promo))
    print(Order(joe, cart, large_order_promo))

    # best_promo
    print(Order(joe, long_order, best_promo))
    print(Order(joe, banana_cart, best_promo))
    print(Order(ann, cart, best_promo))
