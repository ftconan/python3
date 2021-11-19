"""
@author: magician
@file:   redis_action_ch03.py
@date:   2021/11/16
"""
import threading
import time

import redis

ONE_WEEK_IN_SECONDS = 7 * 86400
VOTE_SCORE = 432
ARTICLES_PER_PAGE = 25
THIRTY_DAYS = 30*86400


def update_token(conn, token, user, item=None):
    """
    修改token
    @param conn:
    @param token:
    @param user:
    @param item:
    @return:
    """
    timestamp = time.time()
    conn.hset('login:', token, user)
    conn.zadd('recent:', token, timestamp)

    if item:
        key = 'viewed:' + token
        conn.lrem(key, item)
        conn.rpush(key, item)
        conn.ltrim(key, -25, -1)
        conn.zincrby('viewed:', item, -1)


def publisher(conn, n):
    """
    发布者
    @param conn:
    @param n:
    @return:
    """
    time.sleep(1)
    for i in range(n):
        conn.publish('channel', i)
        time.sleep(1)


def run_pubsub(conn):
    """
    pubsub
    @param conn:
    @return:
    """
    threading.Thread(target=publisher, args=(3,)).start()
    pubsub = conn.pubsub
    pubsub.subscribe(['channel'])
    count = 0
    for item in pubsub.listen():
        print(item)
        count += 1
        if count == 4:
            pubsub.unsubscribe()
        if count == 5:
            break


def article_vote(conn, user, article):
    """
    文章投票
    @param conn:
    @param user:
    @param article:
    @return:
    """
    cutoff = time.time() - ONE_WEEK_IN_SECONDS
    posted = conn.zscore('time:', article)
    if posted < cutoff:
        return

    article_id = article.partition(':')[-1]
    pipeline = conn.pipeline()
    pipeline.sadd('voted:' + article_id, user)
    pipeline.expire('voted:' + article_id, int(posted - cutoff))
    if pipeline.execute()[0]:
        pipeline.zincrby('score:', article, VOTE_SCORE)
        pipeline.hincrby(article, 'votes', 1)
        pipeline.execute()


def article_vote1(conn, user, article):
    """
    文章投票1
    @param conn:
    @param user:
    @param article:
    @return:
    """
    cutoff = time.time() - ONE_WEEK_IN_SECONDS
    posted = conn.zscore('time:', article)
    article_id = article.partition(':')[-1]
    voted = 'voted:' + article_id

    pipeline = conn.pipeline()
    while posted > cutoff:
        try:
            pipeline.watch(voted)
            if not pipeline.sismember(voted, article):
                pipeline.multi()
                pipeline.sadd(voted, user)
                pipeline.expire(voted, int(posted-cutoff))
                pipeline.zincrby('score:', article, VOTE_SCORE)
                pipeline.hincrby(article, 'votes', 1)
                pipeline.execute()
            else:
                pipeline.unwatch()

            return
        except redis.exceptions.WatchError:
            cutoff = time.time() - ONE_WEEK_IN_SECONDS


def get_articles(conn, page, order='score:'):
    """
    get_articles
    @param conn:
    @param page:
    @param order:
    @return:
    """
    start = max(page-1, 0) * ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE - 1

    ids = conn.zrevrangebyscore(order, start, end)

    pipeline = conn.pipeline()
    all(map(pipeline.hgetall, ids))

    articles = []
    for id, article_data in zip(ids, pipeline.execute()):
        article_data['id'] = id
        articles.append(article_data)

    return articles


def check_token(conn, token):
    """
    check_token
    @param conn:
    @param token:
    @return:
    """
    return conn.get('login:' + token)


def update_token1(conn, token, user, item=None):
    """
    update_token1
    @param conn:
    @param token:
    @param user:
    @param item:
    @return:
    """
    conn.setex('login:' + token, user, THIRTY_DAYS)
    key = 'viewed:' + token
    if item:
        conn.lrem(key, item)
        conn.rpush(key, item)
        conn.ltrim(key, -25, -1)
        conn.zincrby('viewed:', item, -1)
    conn.expire(key, THIRTY_DAYS)


def add_to_cart(conn, session, item, count):
    """
    add_to_cart
    @param conn:
    @param session:
    @param item:
    @param count:
    @return:
    """
    key = 'cart:' + session
    if count <= 0:
        conn.hrem(key, item)
    else:
        conn.hset(key, item, count)
    conn.expire(key, THIRTY_DAYS)
