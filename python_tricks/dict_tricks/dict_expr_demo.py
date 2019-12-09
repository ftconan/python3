"""
    @author: magician
    @date: 2019/12/9
    @file: dict_expr_demo.py
"""


class AlwaysEquals:
    """
    AlwaysEquals
    """

    def __eq__(self, other):
        return True

    def __hash__(self):
        return id(self)


class SameHash:
    """
    SameHash
    """
    def __hash__(self):
        return 1


if __name__ == '__main__':
    print({True: 'yes', 1: 'no', 1.0: 'maybe'})
    print(['no', 'yes'][True])

    print(AlwaysEquals() == AlwaysEquals())
    print(AlwaysEquals() == 42)
    print(AlwaysEquals() == 'waat?')
    objects = [AlwaysEquals(), AlwaysEquals(), AlwaysEquals()]
    print([hash(obj) for obj in objects])
    print({AlwaysEquals(): 'yes', AlwaysEquals(): 'no'})

    a = SameHash()
    b = SameHash()
    print(a == b)
    print(hash(a), hash(b))
    print({a: 'a', b: 'b'})
