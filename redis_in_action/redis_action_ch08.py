"""
@author: magician
@file:   redis_action_ch08.py
@date:   2021/12/8
"""
import cgi
import functools
import http.server
import json
import random
import socket
import socketserver
import threading
import time
import unittest
import urllib.parse
import uuid

import math
import redis


def to_bytes(x):
    return x.encode() if isinstance(x, str) else x


def to_str(x):
    return x.decode() if isinstance(x, bytes) else x


def acquire_lock_with_timeout(
        conn, lockname, acquire_timeout=10, lock_timeout=10):
    identifier = str(uuid.uuid4())
    lockname = 'lock:' + lockname
    lock_timeout = int(math.ceil(lock_timeout))

    end = time.time() + acquire_timeout
    while time.time() < end:
        if conn.setnx(lockname, identifier):
            conn.expire(lockname, lock_timeout)
            return identifier
        elif conn.ttl(lockname) < 0:
            conn.expire(lockname, lock_timeout)

        time.sleep(.001)

    return False


def release_lock(conn, lockname, identifier):
    pipe = conn.pipeline(True)
    lockname = 'lock:' + lockname
    identifier = to_bytes(identifier)

    while True:
        try:
            pipe.watch(lockname)
            if pipe.get(lockname) == identifier:
                pipe.multi()
                pipe.delete(lockname)
                pipe.execute()
                return True

            pipe.unwatch()
            break

        except redis.exceptions.WatchError:
            pass

    return False


CONFIGS = {}
CHECKED = {}


def get_config(conn, type, component, wait=1):
    key = 'config:%s:%s' % (type, component)

    if CHECKED.get(key) < time.time() - wait:
        CHECKED[key] = time.time()
        config = json.loads(conn.get(key) or '{}')
        old_config = CONFIGS.get(key)

        if config != old_config:
            CONFIGS[key] = config

    return CONFIGS.get(key)


REDIS_CONNECTIONS = {}


def redis_connection(component, wait=1):
    key = 'config:redis:' + component

    def wrapper(function):
        @functools.wraps(function)
        def call(*args, **kwargs):
            old_config = CONFIGS.get(key, object())
            _config = get_config(old_config, 'redis', component, wait)

            config = {}
            for k, v in _config.items():
                config[k.encode('utf-8')] = v

            if config != old_config:
                REDIS_CONNECTIONS[key] = redis.Redis(**config)

            return function(
                REDIS_CONNECTIONS.get(key), *args, **kwargs)

        return call

    return wrapper


def execute_later(conn, queue, name, args):
    # this is just for testing purposes
    assert conn is args[0]
    t = threading.Thread(target=globals()[name], args=tuple(args))
    t.setDaemon(True)
    t.start()


def create_user(conn, login, name):
    """
    create_user
    @param conn:
    @param login:
    @param name:
    @return:
    """
    llogin = login.lower()
    lock = acquire_lock_with_timeout(conn, 'user:' + llogin, 1)
    if not lock:
        return None

    if conn.hget('users:', llogin):
        release_lock(conn, 'user:' + llogin, lock)
        return None

    id = conn.incr('user:id:')
    pipeline = conn.pipeline(True)
    pipeline.hset('users:', llogin, id)
    pipeline.hmset('user:%s' % id, {
        'login': login,
        'id': id,
        'name': name,
        'followers': 0,
        'following': 0,
        'posts': 0,
        'signup': time.time(),
    })
    pipeline.execute()
    release_lock(conn, 'user:' + llogin, lock)

    return id


def create_status(conn, uid, message, **data):
    """
    create_status
    @param conn:
    @param uid:
    @param message:
    @param data:
    @return:
    """
    pipeline = conn.pipeline(True)
    pipeline.hget('user:%s' % uid, 'login')
    pipeline.hincrby('status:id:')
    login, id = pipeline.execute()

    if not login:
        return None

    data.update({
        'message': message,
        'posted': time.time(),
        'id': id,
        'uid': uid,
        'login': login,
    })
    pipeline.hmset('status:%s' % id, data)
    pipeline.hincrby('user:%s' % uid, 'posts')
    pipeline.execute()

    return id


def get_status_messages(conn, uid, timeline='home:', page=1, count=30):
    """
    get_status_messages
    @param conn:
    @param uid:
    @param timeline:
    @param page:
    @param count:
    @return:
    """
    statuses = conn.zrevrange('%s%s' % (timeline, uid), (page - 1) * count, page * count - 1)
    pipeline = conn.pipeline(True)
    for id in statuses:
        pipeline.hgetall('statuses:%s' % (to_str(id),))

    return [_f for _f in pipeline.execute() if _f]


HOME_TIMELINE_SIZE = 1000


def follow_user(conn, uid, other_uid):
    """
    follow_user
    @param conn:
    @param uid:
    @param other_uid:
    @return:
    """
    fkey1 = 'following:%s' % uid
    fkey2 = 'followers:%s' % other_uid

    if conn.zscore(fkey1, other_uid):
        return None

    now = time.time()

    pipeline = conn.pipeline(True)
    pipeline.zadd(fkey1, {other_uid: now})
    pipeline.zadd(fkey2, {uid: now})
    pipeline.zrevrange('profile:%s' % other_uid, 0, HOME_TIMELINE_SIZE - 1, withscores=True)
    following, followers, status_and_score = pipeline.execute()[-3:]

    pipeline.hincrby('user:%s' % uid, 'following', int(following))
    pipeline.hincrby('user:%s' % other_uid, 'followers', int(followers))
    if status_and_score:
        pipeline.zadd('home:%s' % uid, dict(status_and_score))
    pipeline.zremrangebyrank('home:%s' % uid, 0, -HOME_TIMELINE_SIZE - 1)
    pipeline.execute()

    return True


def unfollow_user(conn, uid, other_uid):
    """
    unfollow_user
    @param conn:
    @param uid:
    @param other_uid:
    @return:
    """
    fkey1 = 'following:%s' % uid
    fkey2 = 'followers:%s' % other_uid

    if conn.zcard(fkey1, other_uid):
        return None

    pipeline = conn.pipeline(True)
    pipeline.zrem(fkey1, other_uid)
    pipeline.zrem(fkey2, uid)
    pipeline.zrevrange('profile:%s' % other_uid, 0, HOME_TIMELINE_SIZE - 1, withscores=True)
    following, followers, statuses = pipeline.execute()[-3:]

    pipeline.hincrby('user:%s' % uid, 'following', -int(following))
    pipeline.hincrby('user:%s' % other_uid, 'followers', -int(followers))
    if statuses:
        pipeline.zrem('home:%s' % uid, statuses)
    pipeline.execute()

    return True


REFILL_USERS_STEP = 50


def refill_timeline(conn, incoming, timeline, start=0):
    """
    refill_timeline
    @param conn:
    @param incoming:
    @param timeline:
    @param start:
    @return:
    """
    if not start and conn.zcard(timeline) >= 750:
        return

    users = conn.zrangebyscore(incoming, start, 'inf',
                               start=0, num=REFILL_USERS_STEP, withscores=True)

    pipeline = conn.pipeline(False)
    for uid, start in users:
        uid = to_str(uid)
        pipeline.zrevrange('profile:%s' % uid,
                           0, HOME_TIMELINE_SIZE - 1, withscores=True)

    messages = []
    for results in pipeline.execute():
        messages.extend(results)

    messages.sort(key=lambda x: -x[1])
    del messages[HOME_TIMELINE_SIZE:]

    pipeline = conn.pipeline(True)
    if messages:
        pipeline.zadd(timeline, dict(messages))
    pipeline.zremrangebyrank(
        timeline, 0, -HOME_TIMELINE_SIZE - 1)
    pipeline.execute()

    if len(users) >= REFILL_USERS_STEP:
        execute_later(conn, 'default', 'refill_timeline',
                      [conn, incoming, timeline, start])


def follow_user_list(conn, other_uid, list_id):
    fkey1 = 'list:in:%s' % list_id
    fkey2 = 'list:out:%s' % other_uid
    timeline = 'list:statuses:%s' % list_id

    if conn.zscore(fkey1, other_uid):
        return None

    now = time.time()

    pipeline = conn.pipeline(True)
    pipeline.zadd(fkey1, {other_uid: now})
    pipeline.zadd(fkey2, {list_id: now})
    pipeline.zrevrange('profile:%s' % other_uid,
                       0, HOME_TIMELINE_SIZE - 1, withscores=True)
    following, followers, status_and_score = pipeline.execute()[-3:]

    pipeline.hincrby('list:%s' % list_id, 'following', int(following))
    pipeline.zadd(timeline, dict(status_and_score))
    pipeline.zremrangebyrank(timeline, 0, -HOME_TIMELINE_SIZE - 1)

    pipeline.execute()
    return True


def unfollow_user_list(conn, other_uid, list_id):
    fkey1 = 'list:in:%s' % list_id
    fkey2 = 'list:out:%s' % other_uid
    timeline = 'list:statuses:%s' % list_id

    if not conn.zscore(fkey1, other_uid):
        return None

    pipeline = conn.pipeline(True)
    pipeline.zrem(fkey1, other_uid)
    pipeline.zrem(fkey2, list_id)
    pipeline.zrevrange('profile:%s' % other_uid,
                       0, HOME_TIMELINE_SIZE - 1)
    following, followers, statuses = pipeline.execute()[-3:]

    pipeline.hincrby('list:%s' % list_id, 'following', -int(following))
    if statuses:
        pipeline.zrem(timeline, *statuses)
        refill_timeline(fkey1, timeline)

    pipeline.execute()
    return True


def create_user_list(conn, uid, name):
    pipeline = conn.pipeline(True)
    pipeline.hget('user:%s' % uid, 'login')
    pipeline.incr('list:id:')
    login, id = pipeline.execute()

    if not login:
        return None

    now = time.time()

    pipeline = conn.pipeline(True)
    pipeline.zadd('lists:%s' % uid, {id: now})
    pipeline.hmset('list:%s' % id, {
        'name': name,
        'id': id,
        'uid': uid,
        'login': login,
        'following': 0,
        'created': now,
    })
    pipeline.execute()

    return id


def post_status(conn, uid, message, **data):
    id = create_status(conn, uid, message, **data)
    if not id:
        return None

    posted = conn.hget('status:%s' % id, 'posted')
    if not posted:
        return None

    post = {str(id): float(posted)}
    conn.zadd('profile:%s' % uid, post)

    syndicate_status(conn, uid, post)
    return id


POSTS_PER_PASS = 1000


def syndicate_status(conn, uid, post, start=0):
    followers = conn.zrangebyscore('followers:%s' % uid, start, 'inf',
                                   start=0, num=POSTS_PER_PASS, withscores=True)

    pipeline = conn.pipeline(False)
    for follower, start in followers:
        follower = to_str(follower)
        pipeline.zadd('home:%s' % follower, post)
        pipeline.zremrangebyrank(
            'home:%s' % follower, 0, -HOME_TIMELINE_SIZE - 1)
    pipeline.execute()

    if len(followers) >= POSTS_PER_PASS:
        execute_later(conn, 'default', 'syndicate_status',
                      [conn, uid, post, start])


def syndicate_status_list(conn, uid, post, start=0, on_lists=False):
    key = 'followers:%s' % uid
    base = 'home:%s'
    if on_lists:
        key = 'list:out:%s' % uid
        base = 'list:statuses:%s'
    followers = conn.zrangebyscore(key, start, 'inf',
                                   start=0, num=POSTS_PER_PASS, withscores=True)

    pipeline = conn.pipeline(False)
    for follower, start in followers:
        follower = to_str(follower)
        pipeline.zadd(base % follower, post)
        pipeline.zremrangebyrank(
            base % follower, 0, -HOME_TIMELINE_SIZE - 1)
    pipeline.execute()

    if len(followers) >= POSTS_PER_PASS:
        execute_later(conn, 'default', 'syndicate_status',
                      [conn, uid, post, start, on_lists])

    elif not on_lists:
        execute_later(conn, 'default', 'syndicate_status',
                      [conn, uid, post, 0, True])


def delete_status(conn, uid, status_id):
    status_id = to_str(status_id)
    key = 'status:%s' % status_id
    lock = acquire_lock_with_timeout(conn, key, 1)
    if not lock:
        return None

    if conn.hget(key, 'uid') != to_bytes(uid):
        release_lock(conn, key, lock)
        return None

    uid = to_str(uid)
    pipeline = conn.pipeline(True)
    pipeline.delete(key)
    pipeline.zrem('profile:%s' % uid, status_id)
    pipeline.zrem('home:%s' % uid, status_id)
    pipeline.hincrby('user:%s' % uid, 'posts', -1)
    pipeline.execute()

    release_lock(conn, key, lock)
    return True


def clean_timelines(conn, uid, status_id, start=0, on_lists=False):
    uid = to_str(uid)
    status_id = to_str(status_id)
    key = 'followers:%s' % uid
    base = 'home:%s'
    if on_lists:
        key = 'list:out:%s' % uid
        base = 'list:statuses:%s'
    followers = conn.zrangebyscore(key, start, 'inf',
                                   start=0, num=POSTS_PER_PASS, withscores=True)

    pipeline = conn.pipeline(False)
    for follower, start in followers:
        follower = to_str(follower)
        pipeline.zrem(base % follower, status_id)
    pipeline.execute()

    if len(followers) >= POSTS_PER_PASS:
        execute_later(conn, 'default', 'clean_timelines',
                      [conn, uid, status_id, start, on_lists])

    elif not on_lists:
        execute_later(conn, 'default', 'clean_timelines',
                      [conn, uid, status_id, 0, True])


class StreamingAPIServer(
    socketserver.ThreadingMixIn,
    http.server.HTTPServer):
    daemon_threads = True


class StreamingAPIRequestHandler(
    http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parse_identifier(self)
        if self.path != '/statuses/sample.json':
            return self.send_error(404)

        process_filters(self)

    def do_POST(self):
        parse_identifier(self)
        if self.path != '/statuses/filter.json':
            return self.send_error(404)

        process_filters(self)


def parse_identifier(handler):
    handler.identifier = None
    handler.query = {}
    if '?' in handler.path:
        handler.path, _, query = handler.path.partition('?')
        handler.query = urllib.parse.parse_qs(query)
        identifier = handler.query.get('identifier') or [None]
        handler.identifier = identifier[0]


FILTERS = ('track', 'filter', 'location')


def process_filters(handler):
    id = handler.identifier
    if not id:
        return handler.send_error(401, "identifier missing")

    method = handler.path.rsplit('/')[-1].split('.')[0]
    name = None
    args = None
    if method == 'filter':
        data = cgi.FieldStorage(
            fp=handler.rfile,
            headers=handler.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': handler.headers['Content-Type'],
                     })

        for name in data:
            if name in FILTERS:
                args = data.getfirst(name).lower().split(',')
                break

        if not args:
            return handler.send_error(401, "no filter provided")
    else:
        args = handler.query

    handler.send_response(200)
    handler.send_header('Transfer-Encoding', 'chunked')
    handler.end_headers()

    quit = [False]
    for item in filter_content(id, method, name, args, quit):
        try:
            handler.wfile.write('%X\r\n%s\r\n' % (len(item), item))
        except socket.error:
            quit[0] = True
    if not quit[0]:
        handler.wfile.write('0\r\n\r\n')


_create_status = create_status


def create_status(conn, uid, message, **data):
    pipeline = conn.pipeline(True)
    pipeline.hget('user:%s' % uid, 'login')
    pipeline.incr('status:id:')
    login, id = pipeline.execute()

    if not login:
        return None

    data.update({
        'message': message,
        'posted': time.time(),
        'id': id,
        'uid': uid,
        'login': to_str(login),
    })
    pipeline.hmset('status:%s' % id, data)
    pipeline.hincrby('user:%s' % uid, 'posts')
    pipeline.publish('streaming:status:', json.dumps(data))  # A
    pipeline.execute()
    return id


_delete_status = delete_status


def delete_status(conn, uid, status_id):
    # raise Exception("what the fuck")
    status_id = to_str(status_id)
    key = 'status:%s' % status_id
    lock = acquire_lock_with_timeout(conn, key, 1)
    if not lock:
        return None

    if conn.hget(key, 'uid') != to_bytes(uid):
        release_lock(conn, key, lock)
        return None

    uid = to_str(uid)
    pipeline = conn.pipeline(True)
    status = conn.hgetall(key)
    status = {to_str(k): to_str(v) for k, v in status.items()}
    status['deleted'] = True
    pipeline.publish('streaming:status:', json.dumps(status))
    pipeline.delete(key)
    pipeline.zrem('profile:%s' % uid, status_id)
    pipeline.zrem('home:%s' % uid, status_id)
    pipeline.hincrby('user:%s' % uid, 'posts', -1)
    pipeline.execute()

    release_lock(conn, key, lock)
    return True


@redis_connection('social-network')
def filter_content(conn, id, method, name, args, quit):
    match = create_filters(id, method, name, args)

    pubsub = conn.pubsub()
    pubsub.subscribe(['streaming:status:'])

    for item in pubsub.listen():
        message = item['data']
        decoded = json.loads(message)

        if match(decoded):
            if decoded.get('deleted'):
                yield json.dumps({
                    'id': decoded['id'], 'deleted': True})
            else:
                yield message

        if quit[0]:
            break

    pubsub.reset()


def create_filters(id, method, name, args):
    if method == 'sample':
        return SampleFilter(id, args)
    elif name == 'track':
        return TrackFilter(args)
    elif name == 'follow':
        return FollowFilter(args)
    elif name == 'location':
        return LocationFilter(args)
    raise Exception("Unknown filter")


def SampleFilter(id, args):
    percent = int(args.get('percent', ['10'])[0], 10)
    ids = list(range(100))
    shuffler = random.Random(id)
    shuffler.shuffle(ids)
    keep = set(ids[:max(percent, 1)])

    def check(status):
        return (status['id'] % 100) in keep

    return check


def TrackFilter(list_of_strings):
    groups = []
    for group in list_of_strings:
        group = set(group.lower().split())
        if group:
            groups.append(group)

    def check(status):
        message_words = set(status['message'].lower().split())
        for group in groups:
            if len(group & message_words) == len(group):
                return True
        return False

    return check


def FollowFilter(names):
    nset = set()
    for name in names:
        nset.add('@' + name.lower().lstrip('@'))

    def check(status):
        message_words = set(status['message'].lower().split())
        message_words.add('@' + status['login'].lower())

        return message_words & nset

    return check


def LocationFilter(list_of_boxes):
    boxes = []
    for start in range(0, len(list_of_boxes) - 3, 4):
        boxes.append(list(map(float, list_of_boxes[start:start + 4])))

    def check(self, status):
        location = status.get('location')
        if not location:
            return False

        lat, lon = list(map(float, location.split(',')))
        for box in self.boxes:
            if (box[1] <= lat <= box[3] and
                    box[0] <= lon <= box[2]):
                return True
        return False

    return check


_filter_content = filter_content


def filter_content(identifier, method, name, args, quit):
    print("got:", identifier, method, name, args)
    for i in range(10):
        yield json.dumps({'id': i})
        if quit[0]:
            break
        time.sleep(.1)


class TestCh08(unittest.TestCase):
    def setUp(self):
        self.conn = redis.Redis(db=15, password='123456')
        self.conn.flushdb()

    def tearDown(self):
        self.conn.flushdb()

    def test_create_user_and_status(self):
        self.assertEqual(create_user(self.conn, 'TestUser', 'Test User'), 1)
        self.assertEqual(create_user(self.conn, 'TestUser', 'Test User2'), None)

        self.assertEqual(create_status(self.conn, 1, "This is a new status message"), 1)
        self.assertEqual(self.conn.hget('user:1', 'posts'), b'1')

    def test_follow_unfollow_user(self):
        self.assertEqual(create_user(self.conn, 'TestUser', 'Test User'), 1)
        self.assertEqual(create_user(self.conn, 'TestUser2', 'Test User2'), 2)

        self.assertTrue(follow_user(self.conn, 1, 2))
        self.assertEqual(self.conn.zcard('followers:2'), 1)
        self.assertEqual(self.conn.zcard('followers:1'), 0)
        self.assertEqual(self.conn.zcard('following:1'), 1)
        self.assertEqual(self.conn.zcard('following:2'), 0)
        self.assertEqual(self.conn.hget('user:1', 'following'), b'1')
        self.assertEqual(self.conn.hget('user:2', 'following'), b'0')
        self.assertEqual(self.conn.hget('user:1', 'followers'), b'0')
        self.assertEqual(self.conn.hget('user:2', 'followers'), b'1')

        self.assertEqual(unfollow_user(self.conn, 2, 1), None)
        self.assertEqual(unfollow_user(self.conn, 1, 2), True)
        self.assertEqual(self.conn.zcard('followers:2'), 0)
        self.assertEqual(self.conn.zcard('followers:1'), 0)
        self.assertEqual(self.conn.zcard('following:1'), 0)
        self.assertEqual(self.conn.zcard('following:2'), 0)
        self.assertEqual(self.conn.hget('user:1', 'following'), b'0')
        self.assertEqual(self.conn.hget('user:2', 'following'), b'0')
        self.assertEqual(self.conn.hget('user:1', 'followers'), b'0')
        self.assertEqual(self.conn.hget('user:2', 'followers'), b'0')

    def test_syndicate_status(self):
        self.assertEqual(create_user(self.conn, 'TestUser', 'Test User'), 1)
        self.assertEqual(create_user(self.conn, 'TestUser2', 'Test User2'), 2)
        self.assertTrue(follow_user(self.conn, 1, 2))
        self.assertEqual(self.conn.zcard('followers:2'), 1)
        self.assertEqual(self.conn.hget('user:1', 'following'), b'1')
        self.assertEqual(post_status(self.conn, 2, 'this is some message content'), 1)
        self.assertEqual(len(get_status_messages(self.conn, 1)), 1)

        for i in range(3, 11):
            self.assertEqual(create_user(self.conn, 'TestUser%s' % i, 'Test User%s' % i), i)
            follow_user(self.conn, i, 2)

        global POSTS_PER_PASS
        POSTS_PER_PASS = 5

        self.assertEqual(post_status(self.conn, 2, 'this is some other message content'), 2)
        time.sleep(.1)
        self.assertEqual(len(get_status_messages(self.conn, 9)), 2)

        self.assertTrue(unfollow_user(self.conn, 1, 2))
        self.assertEqual(len(get_status_messages(self.conn, 1)), 0)

    def test_refill_timeline(self):
        self.assertEqual(create_user(self.conn, 'TestUser', 'Test User'), 1)
        self.assertEqual(create_user(self.conn, 'TestUser2', 'Test User2'), 2)
        self.assertEqual(create_user(self.conn, 'TestUser3', 'Test User3'), 3)

        self.assertTrue(follow_user(self.conn, 1, 2))
        self.assertTrue(follow_user(self.conn, 1, 3))

        global HOME_TIMELINE_SIZE
        HOME_TIMELINE_SIZE = 5

        for i in range(10):
            self.assertTrue(post_status(self.conn, 2, 'message'))
            self.assertTrue(post_status(self.conn, 3, 'message'))
            time.sleep(.05)

        self.assertEqual(len(get_status_messages(self.conn, 1)), 5)
        self.assertTrue(unfollow_user(self.conn, 1, 2))
        self.assertTrue(len(get_status_messages(self.conn, 1)) < 5)

        refill_timeline(self.conn, 'following:1', 'home:1')
        messages = get_status_messages(self.conn, 1)
        self.assertEqual(len(messages), 5)
        for msg in messages:
            self.assertEqual(msg[b'uid'], b'3')

        delete_status(self.conn, '3', messages[-1][b'id'])
        self.assertEqual(len(get_status_messages(self.conn, 1)), 4)
        self.assertEqual(self.conn.zcard('home:1'), 5)
        clean_timelines(self.conn, '3', messages[-1][b'id'])
        self.assertEqual(self.conn.zcard('home:1'), 4)


if __name__ == '__main__':
    unittest.main()
