"""
    @author: magician
    @date: 2019/12/2
    @file: loop_demo.py
"""


if __name__ == '__main__':
    my_items = ['a', 'b', 'c']

    # C style
    i = 0
    while i < len(my_items):
        print(my_items[i])
        i += 1

    print(range(len(my_items)))
    print(list(range(0, 3)))

    for i in range(len(my_items)):
        print(my_items[i])

    # pythonic
    for item in my_items:
        print(item)

    for i, item in enumerate(my_items):
        print('{0}:{1}'.format(i, item))

    emails = {
        'Bob': 'bob@example.com',
        'Alice': 'alice@example.com'
    }

    for name, email in emails.items():
        print(name, '->', email)

    # JAVA style
    # for (int i = a; i < n; i += s){
    #     //
    # }

    # for i in range(a, n, s):
    #     pass
