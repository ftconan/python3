"""
    @author: magician
    @date: 2019/12/13
    @file: list_comp_demo.py
"""


if __name__ == '__main__':
    a = list(range(11))
    squares = [x**2 for x in a]
    print(squares)
    squares = map(lambda x: x**2, a)
    even_squares = [x**2 for x in a if x % 2 == 0]
    print(even_squares)
    alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
    assert even_squares == list(alt)

    child_ranks = {'ghost': 1, 'habanero': 2, 'cayenne': 3}
    rank_dict = {rank: name for name, rank in child_ranks.items()}
    child_len_set = {len(name) for name in rank_dict.values()}
    print(rank_dict)
    print(child_len_set)
