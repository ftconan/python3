"""
    @author: magician
    @date: 2019/12/6
    @file: generator_expression_demo.py
"""


if __name__ == '__main__':
    iterator = ('Hello' for i in range(3))
    for x in iterator:
        print(x)

    # Generator Expressions vs List Comprehension
    listcomp = ['Hello' for i in range(3)]
    genexpr = ('Hello' for i in range(3))
    print(listcomp)
    print(genexpr)

    # print(next(genexpr))
    # print(next(genexpr))
    # print(next(genexpr))
    # try:
    #     print(next(genexpr))
    # except Exception as e:
    #     print(e)
    print(list(genexpr))

    # Filtering Value
    even_squares = (x * x for x in range(10) if x % 2 == 0)
    for x in even_squares:
        print(x)

    # In-line Generator Expressions
    for x in ('Bom dia' for i in range(3)):
        print(x)
    print(sum((x * 2 for x in range(10))))
    print(sum(x * 2 for x in range(10)))

    # Too Much of a Good Thing...
    pass
