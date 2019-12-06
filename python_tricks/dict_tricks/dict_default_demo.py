"""
    @author: magician
    @date: 2019/12/6
    @file: dict_default_demo.py
"""


def greeting(userid):
    """
    greeting
    :param userid:
    :return:
    """
    # return 'Hi {0}!'.format(name_for_userid[userid] if userid in name_for_userid else 'there')
    # try:
    #     return 'Hi {0}!'.format(name_for_userid[userid])
    # except KeyError:
    #     return 'Hi there!'

    return 'Hi {0}!'.format(name_for_userid.get(userid, 'there'))


if __name__ == '__main__':
    name_for_userid = {
        382: 'Alice',
        950: 'Bob',
        590: 'Dilbert',
    }
    print(greeting(382))
    print(greeting(22))
