"""
    @author: magician
    @date: 2019/12/3
    @file: slice_demo.py
"""


if __name__ == '__main__':
    lst = [1, 2, 3, 4, 5]
    print(lst)
    print(lst[1:3:1])
    print(lst[1:3])
    print(lst[::2])
    print(lst[::-1])

    # del lst[:]
    # print(lst)
    # lst.clear()

    original_lst = lst
    lst[:] = [7, 8, 9]
    print(lst)
    print(original_lst)
    print(original_lst is lst)

    copied_lst = lst[:]
    print(copied_lst)
    print(copied_lst is lst)
