"""
@author: magician
@file:   redis_action_ch02.py
@date:   2021/11/15
"""
import json
import threading
import time
import unittest
import urllib.parse
import uuid

QUIT = False
LIMIT = 10000000


def to_bytes(x):
    """
    str -> bytes
    @param x:
    @return:
    """
    return x.encode() if isinstance(x, str) else x


def to_str(x):
    """
    bytes -> str
    @param x:
    @return:
    """
    return x.decode() if isinstance(x, bytes) else x


def check_token(conn, token):
    """
    检查token
    @param conn:
    @param token:
    @return:
    """
    return conn.hget('login:', token)


def update_token1(conn, token, user, item=None):
    """
    更新token
    @param conn:
    @param token:
    @param user:
    @param item:
    @return:
    """
    timestamp = time.time()
    conn.hset('login:', token, user)
    conn.zadd('recent:', {token: timestamp})

    if item:
        conn.zadd('viewed:' + token, {item: timestamp})
        conn.zremrangebyrank('viewed:' + token, 0, -26)


def clean_sessions(conn):
    """
    清除session
    @param conn:
    @return:
    """
    while not QUIT:
        size = conn.zcard('recent:')
        if size <= LIMIT:
            time.sleep(1)
            continue

        end_index = min(size - LIMIT, 100)
        tokens = conn.zrange('recent:', 0, end_index-1)

        session_keys = []
        for token in tokens:
            token = to_str(token)
            session_keys.append('viewed:' + token)

        conn.delete(*session_keys)
        conn.hdel('login:', *tokens)
        conn.zrem('recent:', *tokens)


def add_to_cart(conn, session, item, count):
    """
    添加到购物车
    @param conn:
    @param session:
    @param item:
    @param count:
    @return:
    """
    if count < 0:
        conn.hrem('cart:' + session, item)
    else:
        conn.hset('cart:' + session, item, count)


def clean_full_sessions(conn):
    """
    清楚完整sessions
    @param conn:
    @return:
    """
    while not QUIT:
        size = conn.zcard('recent:')
        if size <= LIMIT:
            time.sleep(1)
            continue

        end_index = min(size - LIMIT, 100)
        sessions = conn.zrange('recent:', 0, end_index-1)

        session_keys = []
        for sess in sessions:
            sess = to_str(sess)
            session_keys.append('viewed:' + sess)
            session_keys.append('cart:' + sess)

        conn.delete(*session_keys)
        conn.hdel('login:', *sessions)
        conn.zrem('recent:', *sessions)


def cache_request(conn, request, callback):
    """
    缓存请求
    @param conn:
    @param request:
    @param callback:
    @return:
    """
    if not can_cache(conn, request):
        return callback(request)

    page_key = 'cache:' + hash_request(request)
    content = conn.get(page_key)

    if not content:
        content = callback(request)
        conn.setex(page_key, 300, content)

    return content


def schedule_row_cache(conn, row_id, delay):
    """
    定时行缓存
    @param conn:
    @param row_id:
    @param delay:
    @return:
    """
    conn.zadd('delay:', {row_id: delay})
    conn.zadd('schedule:', {row_id: time.time()})


def cache_rows(conn):
    """
    缓存行
    @param conn:
    @return:
    """
    while not QUIT:
        next = conn.zrange('schedule:', 0, 0, withscores=True)
        now = time.time()
        if not next or next[0][1] > now:
            time.sleep(0.05)
            continue

        row_id = next[0][0]
        row_id = to_str(row_id)
        delay = conn.zscore('delay:', row_id)
        if delay <= 0:
            conn.zrem('delay:', row_id)
            conn.zrem('schedule:', row_id)
            conn.delete('inv:' + row_id)
            continue

        row = Inventory.get(row_id)
        conn.zadd('schedule:', {row_id: now + delay})
        row = {to_str(k): to_str(v) for k, v in row.to_dict().items()}
        conn.set('inv:' + row_id, json.dumps(row))


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
    conn.zadd('recent:', {token: timestamp})
    if item:
        conn.zadd('viewed:' + token, {item: timestamp})
        conn.zremrangebyrank('viewed:' + token, 0, -26)
        conn.zincrby('viewed:', -1, item)


def rescale_viewed(conn):
    """
    扩展访问商品数据
    @param conn:
    @return:
    """
    while not QUIT:
        conn.zremrangebyrank('viewed:', 20000, -1)
        conn.zinterstore('viewed:', {'viewed:': 0.5})
        time.sleep(300)


def can_cache(conn, request):
    """
    是否缓存
    @param conn:
    @param request:
    @return:
    """
    item_id = extract_item_id(request)
    if not item_id or is_dynamic(request):
        return False
    rank = conn.zrank('viewed:', item_id)

    return rank is not None and rank < 10000


# --------------- Below this line are helpers to test the code ----------------


def extract_item_id(request):
    parsed = urllib.parse.urlparse(request)
    query = urllib.parse.parse_qs(parsed.query)
    return (query.get('item') or [None])[0]


def is_dynamic(request):
    parsed = urllib.parse.urlparse(request)
    query = urllib.parse.parse_qs(parsed.query)
    return '_' in query


def hash_request(request):
    return str(hash(request))


class Inventory(object):
    def __init__(self, id):
        self.id = id

    @classmethod
    def get(cls, id):
        return Inventory(id)

    def to_dict(self):
        return {'id': self.id, 'data': 'data to cache...', 'cached': time.time()}


class TestCh02(unittest.TestCase):
    def setUp(self):
        import redis
        self.conn = redis.Redis(db=15, password='123456')

    def tearDown(self):
        conn = self.conn
        to_del = (
                conn.keys('login:*') + conn.keys('recent:*') + conn.keys('viewed:*') +
                conn.keys('cart:*') + conn.keys('cache:*') + conn.keys('delay:*') +
                conn.keys('schedule:*') + conn.keys('inv:*'))
        if to_del:
            self.conn.delete(*to_del)
        del self.conn
        global QUIT, LIMIT
        QUIT = False
        LIMIT = 10000000
        print()
        print()

    def test_login_cookies(self):
        conn = self.conn
        global LIMIT, QUIT
        token = str(uuid.uuid4())

        update_token(conn, token, 'username', 'itemX')
        print("We just logged-in/updated token:", token)
        print("For user:", 'username')
        print()

        print("What username do we get when we look-up that token?")
        r = check_token(conn, token)
        print(r)
        print()
        self.assertTrue(r)

        print("Let's drop the maximum number of cookies to 0 to clean them out")
        print("We will start a thread to do the cleaning, while we stop it later")

        LIMIT = 0
        t = threading.Thread(target=clean_sessions, args=(conn,))
        t.setDaemon(True)  # to make sure it dies if we ctrl+C quit
        t.start()
        time.sleep(1)
        QUIT = True
        time.sleep(2)
        if t.is_alive():
            raise Exception("The clean sessions thread is still alive?!?")

        s = conn.hlen('login:')
        print("The current number of sessions still available is:", s)
        self.assertFalse(s)

    def test_shopping_cart_cookies(self):
        conn = self.conn
        global LIMIT, QUIT
        token = str(uuid.uuid4())

        print("We'll refresh our session...")
        update_token(conn, token, 'username', 'itemX')
        print("And add an item to the shopping cart")
        add_to_cart(conn, token, "itemY", 3)
        r = conn.hgetall('cart:' + token)
        print("Our shopping cart currently has:", r)
        print()

        self.assertTrue(len(r) >= 1)

        print("Let's clean out our sessions and carts")
        LIMIT = 0
        t = threading.Thread(target=clean_full_sessions, args=(conn,))
        t.setDaemon(True)  # to make sure it dies if we ctrl+C quit
        t.start()
        time.sleep(1)
        QUIT = True
        time.sleep(2)
        if t.is_alive():
            raise Exception("The clean sessions thread is still alive?!?")

        r = conn.hgetall('cart:' + token)
        print("Our shopping cart now contains:", r)

        self.assertFalse(r)

    def test_cache_request(self):
        conn = self.conn
        token = str(uuid.uuid4())

        def callback(request):
            return "content for " + request

        update_token(conn, token, 'username', 'itemX')
        url = 'http://test.com/?item=itemX'
        print("We are going to cache a simple request against", url)
        result = cache_request(conn, url, callback)
        print("We got initial content:", repr(result))
        print()

        self.assertTrue(result)

        print("To test that we've cached the request, we'll pass a bad callback")
        result2 = cache_request(conn, url, None)
        print("We ended up getting the same response!", repr(result2))

        self.assertEqual(to_bytes(result), to_bytes(result2))

        self.assertFalse(can_cache(conn, 'http://test.com/'))
        self.assertFalse(can_cache(conn, 'http://test.com/?item=itemX&_=1234536'))

    def test_cache_rows(self):
        import pprint
        conn = self.conn
        global QUIT

        print("First, let's schedule caching of itemX every 5 seconds")
        schedule_row_cache(conn, 'itemX', 5)
        print("Our schedule looks like:")
        s = conn.zrange('schedule:', 0, -1, withscores=True)
        pprint.pprint(s)
        self.assertTrue(s)

        print("We'll start a caching thread that will cache the data...")
        t = threading.Thread(target=cache_rows, args=(conn,))
        t.setDaemon(True)
        t.start()

        time.sleep(1)
        print("Our cached data looks like:")
        r = conn.get('inv:itemX')
        print(repr(r))
        self.assertTrue(r)
        print()
        print("We'll check again in 5 seconds...")
        time.sleep(5)
        print("Notice that the data has changed...")
        r2 = conn.get('inv:itemX')
        print(repr(r2))
        print()
        self.assertTrue(r2)
        self.assertTrue(r != r2)

        print("Let's force un-caching")
        schedule_row_cache(conn, 'itemX', -1)
        time.sleep(1)
        r = conn.get('inv:itemX')
        print("The cache was cleared?", not r)
        print()
        self.assertFalse(r)

        QUIT = True
        time.sleep(2)
        if t.is_alive():
            raise Exception("The database caching thread is still alive?!?")

    # We aren't going to bother with the top 10k requests are cached, as
    # we already tested it as part of the cached requests test.


if __name__ == '__main__':
    unittest.main()
