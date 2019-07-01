"""
@file: search_engine.py
@author: magician
@date: 2019/07/01
"""
import os
import re

import pylru


class SearchEngineBase(object):
    """
    SearchEngineBase
    """

    def __init__(self):
        pass

    def add_corpus(self, file_path):
        """
        add corpus
        :param file_path:
        :return:
        """
        with open(file_path, 'r') as f:
            text = f.read()
        self.process_corpus(file_path, text)

    def process_corpus(self, id, text):
        """
        process_corpus
        :param id:
        :param text:
        :return:
        """
        raise Exception('process_corpus not implemented.')

    def search(self, query):
        """
        search
        :param query:
        :return:
        """
        raise Exception('search not implemented.')


class SimpleEngine(SearchEngineBase):
    """
    SimpleEngine
    """

    def __init__(self):
        super(SimpleEngine, self).__init__()
        self.__id_to_texts = {}

    def process_corpus(self, id, text):
        """
        process_corpus
        :param id:
        :param text:
        :return:
        """
        self.__id_to_texts[id] = text

    def search(self, query):
        """
        search
        :param query:
        :return:
        """
        results = []
        for id, text in self.__id_to_texts.items():
            if query in text:
                results.append(id)

        return results


class BOWEngine(SearchEngineBase):
    """
    BOWEngine
    """

    def __init__(self):
        super(BOWEngine, self).__init__()
        self.__id_to_words = {}

    def process_corpus(self, id, text):
        """
        process_corpus
        :param id:
        :param text:
        :return:
        """
        self.__id_to_words[id] = text

    def search(self, query):
        """
        search
        :param query:
        :return:
        """
        query_words = self.parse_text_to_words(query)
        results = []
        for id, words in self.__id_to_words.items():
            if self.query_match(query_words, words):
                results.append(id)

        return results

    @staticmethod
    def query_match(query_words, words):
        """
        query match
        :param query_words:
        :param words:
        :return:
        """
        for query_word in query_words:
            if query_word not in words:
                return False

        return True

    @staticmethod
    def parse_text_to_words(text):
        """
        parse text to words
        :param text:
        :return:
        """
        # 使用正则表达式去除标点符号和换行符
        text = re.sub(r'[^\w ]', ' ', text)
        text = text.lower()
        word_list = text.split(' ')
        # 去除空白单词
        word_list = filter(None, word_list)

        return set(word_list)


class BOWInvertedIndexEngine(SearchEngineBase):
    """
    BOWInvertedIndexEngine
    """

    def __init__(self):
        super(BOWInvertedIndexEngine, self).__init__()
        self.inverted_index = {}

    def process_corpus(self, id, text):
        """
        process corpus
        :param id:
        :param text:
        :return:
        """
        words = self.parse_text_to_words(text)
        for word in words:
            if word not in self.inverted_index:
                self.inverted_index[word] = []

            self.inverted_index[word].append(id)

    def search(self, query):
        """
        search
        :param query:
        :return:
        """
        query_words = list(self.parse_text_to_words(query))
        query_words_index = list()
        for _ in query_words:
            query_words_index.append(0)

        # 如果某一个查询单词的倒序索引为空，我们就立刻返回
        for query_word in query_words:
            if query_word not in self.inverted_index:
                return []

        result = []
        while True:
            # 首先,获得当前状态下所有倒序索引的index
            current_ids = []

            for idx, query_word in enumerate(query_words):
                current_index = query_words_index[idx]
                current_inverted_list = self.inverted_index[query_word]

                # 已经遍历到了某一个倒序索引的末尾,结束search
                if current_index >= len(current_inverted_list):
                    return result

                current_ids.append(current_inverted_list[current_index])

            # 然后,如果current_ids的所有元素都一样,那么表明这个单词在这个元素对应的文档中都出现了
            if all(x == current_ids[0] for x in current_ids):
                result.append(current_ids[0])
                query_words_index = [x + 1 for x in query_words_index]
                continue

            # 如果不是,我们把最小的元素加一
            min_val = min(current_ids)
            min_val_pos = current_ids.index(min_val)
            query_words_index[min_val_pos] += 1

    @staticmethod
    def parse_text_to_words(text):
        """
        parse text to words
        :param text:
        :return:
        """
        # 使用正则表达式去除标点符号和换行符
        text = re.sub(r'[^\w ]', ' ', text)
        text = text.lower()
        word_list = text.split(' ')
        # 去除空白单词
        word_list = filter(None, word_list)

        return set(word_list)


class LRUCache(object):
    """
    LRUCache
    """

    def __init__(self, size=32):
        """
        init
        :param size:
        """
        self.cache = pylru.lrucache(size)

    def has(self, key):
        """
        has
        :param key:
        :return:
        """
        return key in self.cache

    def get(self, key):
        """
        get
        :param key:
        :return:
        """
        return self.cache[key]

    def set(self, key, value):
        """
        set
        :param key:
        :param value:
        :return:
        """
        self.cache[key] = value


class BOWInvertedIndexEngineWithCache(BOWInvertedIndexEngine, LRUCache):
    """
    BOWInvertedIndexEngineWithCache
    """

    def __init__(self):
        super(BOWInvertedIndexEngineWithCache, self).__init__()
        LRUCache.__init__(self)

    def search(self, query):
        """
        search
        :param query:
        :return:
        """
        if self.has(query):
            print('cache hit!')
            return self.get(query)

        result = super(BOWInvertedIndexEngineWithCache, self).search(query)
        self.set(query, result)

        return result


def main(search_engine):
    """
    main
    :param search_engine:
    :return:
    """
    file_paths = [os.path.join('../data', fp) for fp in ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt']]

    for file_path in file_paths:
        search_engine.add_corpus(file_path)

    while True:
        print('please input words in search engine:')
        query = input()
        if query == 'exit':
            break

        results = search_engine.search(query)
        print('found {} result(s):'.format(len(results)))

        for result in results:
            print(result)


if __name__ == '__main__':
    # engine = SimpleEngine()
    # engine = BOWEngine()
    # engine = BOWInvertedIndexEngine()
    engine = BOWInvertedIndexEngineWithCache()

    main(engine)
