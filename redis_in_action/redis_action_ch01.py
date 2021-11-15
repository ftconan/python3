"""
@author: magician
@file:   redis_action_ch01.py
@date:   2021/11/15
"""
import time
import unittest

ONE_WEEK_IN_SECONDS = 7 * 86400
VOTE_SCORE = 432
ARTICLES_PER_PAGE = 25


def article_vote(conn, user, article):
    """
    文章投票
    @param conn:
    @param user:
    @param article:
    @return:
    """
    cutoff = time.time() - ONE_WEEK_IN_SECONDS
    if conn.zscore('time:', article) < cutoff:
        return

    article_id = article.partition(':')[-1]
    if conn.sadd('voted:' + article_id, user):
        conn.zincrby('score:', VOTE_SCORE, user)
        conn.hincrby(article, 'votes', 1)


def post_article(conn, user, title, link):
    """
    发布文章
    @param conn:
    @param user:
    @param title:
    @param link:
    @return:
    """
    article_id = str(conn.incr('article:'))

    voted = 'voted:' + article_id
    conn.sadd(voted, user)
    conn.expire(voted, ONE_WEEK_IN_SECONDS)

    now = time.time()
    article = 'article:' + article_id
    conn.hmset(article, {
        'title': title,
        'link': link,
        'poster': user,
        'time': now,
        'votes': 1,
    })

    conn.zadd('score:', {article: now + VOTE_SCORE})
    conn.zadd('time:', {article: now})

    return article_id


def get_articles(conn, page, order='score:'):
    """
    获取文章
    @param conn:
    @param page:
    @param order:
    @return:
    """
    start = (page-1) * ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE - 1

    ids = conn.zrevrange(order, start, end)
    articles = []
    for id in ids:
        article_data = conn.hgetall(id)
        article_data['id'] = id
        articles.append(article_data)

    return articles


def add_remove_groups(conn, article_id, to_add=[], to_remove=[]):
    """
    添加，移除组
    @param conn:
    @param article_id:
    @param to_add:
    @param to_remove:
    @return:
    """
    article = 'article:' + article_id
    for group in to_add:
        conn.sadd('group:' + group, article)
    for group in to_remove:
        conn.srem('group:' + group, article)


def get_group_articles(conn, group, page, order='score:'):
    """
    获取分组文章
    @param conn:
    @param group:
    @param page:
    @param order:
    @return:
    """
    key = order + group
    if not conn.exists(key):
        conn.zinterstore(key, ['group:' + group, order], aggregate='max')
        conn.expire(key, 60)

    return get_articles(conn, page, key)


# --------------- Below this line are helpers to test the code ----------------


class TestCh01(unittest.TestCase):
    def setUp(self):
        import redis
        self.conn = redis.Redis(db=15, password='123456')

    def tearDown(self):
        del self.conn
        print()
        print()

    def test_article_functionality(self):
        conn = self.conn
        import pprint

        article_id = str(post_article(conn, 'username', 'A title', 'http://www.google.com'))
        print("We posted a new article with id:", article_id)
        print()
        self.assertTrue(article_id)

        print("Its HASH looks like:")
        r = conn.hgetall('article:' + article_id)
        print(r)
        print()
        self.assertTrue(r)

        article_vote(conn, 'other_user', 'article:' + article_id)
        print("We voted for the article, it now has votes:", end=' ')
        v = int(conn.hget('article:' + article_id, 'votes'))
        print(v)
        print()
        self.assertTrue(v > 1)

        print("The currently highest-scoring articles are:")
        articles = get_articles(conn, 1)
        pprint.pprint(articles)
        print()

        self.assertTrue(len(articles) >= 1)

        add_remove_groups(conn, article_id, ['new-group'])
        print("We added the article to a new group, other articles include:")
        articles = get_group_articles(conn, 'new-group', 1)
        pprint.pprint(articles)
        print()
        self.assertTrue(len(articles) >= 1)

        to_del = (
            conn.keys('time:*') + conn.keys('voted:*') + conn.keys('score:*') +
            conn.keys('article:*') + conn.keys('group:*')
        )
        if to_del:
            conn.delete(*to_del)


if __name__ == '__main__':
    unittest.main()
