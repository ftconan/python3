"""
@file: class_demo.py
@author: magician
@date: 2019/6/28
"""


class Document(object):
    """
    Document
    """

    WELCOME_STR = 'Welcome! The context for this book is {}.'

    def __init__(self, title, author, context):
        """
        document init
        :param title:
        :param author:
        :param context:
        """
        print('init function called')
        self.title = title
        self.author = author
        self.__context = context

    @classmethod
    def create_empty_book(cls, title, author):
        """
        create empty book
        :param title:
        :param author:
        :return:
        """
        return cls(title=title, author=author, context='nothing')

    def get_context_length(self):
        """
        get context length
        :return:
        """
        return len(self.__context)

    @staticmethod
    def get_welcome(context):
        """
        get welcome
        :param context:
        :return:
        """
        return Document.WELCOME_STR.format(context)

    def intercept_context(self, length):
        """
        intercept context
        :param length:
        :return:
        """
        self.__context = self.__context[:length]


class Entity(object):
    """
    Entity
    """
    def __init__(self, object_type):
        """
        init object type
        :param object_type:
        """
        print('parent class init called')
        self.object_type = object_type

    def get_context_length(self):
        """
        get context length
        :return:
        """
        raise Exception('get_context_length not implemented')

    def print_title(self):
        """
        print title
        :return:
        """
        print(self.title)


class Document1(Entity):
    """
    Document1
    """
    def __init__(self, title, author, context):
        """
        Document1 init
        :param title:
        :param author:
        :param context:
        """
        print('Document class init called')
        Entity.__init__(self, 'document')
        self.title = title
        self.author = author
        self.__context = context

    def get_context_length(self):
        """
        get context length
        :return:
        """
        return len(self.__context)


class Video(Entity):
    """
    Video
    """
    def __init__(self, title, author, video_length):
        """
        Video init
        :param title:
        :param author:
        :param video_length:
        """
        print('Video class init called')
        Entity.__init__(self, 'video')
        self.title = title
        self.author = author
        self.__video_length = video_length

    def get_context_length(self):
        """
        get context length
        :return:
        """
        return self.__video_length


if __name__ == '__main__':
    harry_potter_book = Document('Harry Potter', 'J.K. Rowling',
                                 '...Forever Do not believe anything is capable of thinking independently...')
    print(harry_potter_book.title)
    print(harry_potter_book.author)
    print(harry_potter_book.get_context_length())
    harry_potter_book.intercept_context(10)
    print(harry_potter_book.get_context_length())

    try:
        print(harry_potter_book.__context)
    except Exception as e:
        print(e)

    empty_book = Document.create_empty_book('What Every Man Thinks About Apart from Sex', 'Professor Sheridan Simove')
    print(empty_book.get_context_length())
    print(empty_book.get_welcome('indeed nothing'))

    harry_potter_book = Document1('Harry Potter(Book)', 'J.K. Rowling',
                                  '...Forever Do not believe anything is capable of thinking independently...')
    harry_potter_movie = Video('Harry Potter(Movie)', 'J.K. Rowling', 120)

    harry_potter_book.print_title()
    harry_potter_movie.print_title()
    print(harry_potter_book.get_context_length())
    print(harry_potter_movie.get_context_length())
