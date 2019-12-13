"""
    @author: magician
    @date: 2019/12/13
    @file: zip_demo.py
"""


if __name__ == '__main__':
    names = ['Cecilia', 'Lise', 'Marie']
    letters = [len(n) for n in names]

    longest_name, max_letters = None, 0
    for i in range(len(names)):
        count = letters[i]
        if count > max_letters:
            longest_name = names[i]
            max_letters = count
    print(longest_name)

    for i, name in enumerate(names):
        count = letters[i]
        if count > max_letters:
            longest_name = name
            max_letters = count
    print(longest_name)

    for name, count in zip(names, letters):
        if count > max_letters:
            longest_name = name
            max_letters = count
    print(longest_name)

    names.append('Rosalind')
    for name, count in zip(names, letters):
        print(name)
