"""
@author: magician
@file:   redis_action_ch05.py
@date:   2021/11/22
"""
import bisect
import contextlib
import csv
import functools
import json
import logging
import random
import threading
import time
import unittest
import uuid

import redis

from datetime import datetime

QUIT = False
SAMPLE_COUNT = 100

config_connection = None

SEVERITY = {
    logging.DEBUG: 'debug',
    logging.INFO: 'info',
    logging.WARNING: 'waring',
    logging.ERROR: 'error',
    logging.CRITICAL: 'critical',
}
SEVERITY.update((name, name) for name in list(SEVERITY.values()))

PRECISION = [1, 5, 60, 300, 3600, 18000, 86400]
LAST_CHECKED = None
IS_UNDER_MAINTENANCE = False

CONFIGS = {}
CHECKED = {}

REDIS_CONNECTIONS = {}


def to_bytes(x):
    """
    to_bytes
    @param x:
    @return:
    """
    return x.encode() if isinstance(x, str) else x


def to_str(x):
    """
    to_str
    @param x:
    @return:
    """
    return x.decode() if isinstance(x, bytes) else x


def log_recent(conn, name, message, severity=logging.INFO, pipe=None):
    """
    log_recent
    @param conn:
    @param name:
    @param message:
    @param severity:
    @param pipe:
    @return:
    """
    severity = str(SEVERITY.get(severity, severity)).lower()
    destination = 'recent:%s:%s' % (name, severity)
    message = time.asctime() + ' ' + message
    pipe = pipe or conn.pipeline()
    pipe.lpush(destination, message)
    pipe.ltrim(destination, 0, 99)
    pipe.execute()


def log_common(conn, name, message, severity=logging.INFO, timeout=5):
    """
    log_common
    @param conn:
    @param name:
    @param message:
    @param severity:
    @param timeout:
    @return:
    """
    severity = str(SEVERITY.get(severity, severity)).lower()
    destination = 'common:%s:%s' % (name, severity)
    start_key = destination + ':start'
    pipe = conn.pipeline()
    end = time.time() + timeout

    while time.time() < end:
        try:
            pipe.watch(start_key)
            now = datetime.utcnow().timetuple()
            hour_start = datetime(*now[:4]).isoformat()

            existing = pipe.get(start_key)
            pipe.multi()
            if existing and existing < to_bytes(hour_start):
                pipe.rename(destination, destination + ':last')
                pipe.rename(destination, destination + ':pstart')
                pipe.set(start_key, hour_start)
            elif not existing:
                pipe.set(start_key, hour_start)

            pipe.zincrby(destination, 1, message)
            log_recent(pipe, name, message, severity, pipe)
            return
        except redis.exceptions.WatchError:
            continue


def update_counter(conn, name, count=1, now=None):
    """
    update_counter
    @param conn:
    @param name:
    @param count:
    @param now:
    @return:
    """
    now = now or time.time()
    pipe = conn.pipeline()

    for prec in PRECISION:
        pnow = int(now / prec) * prec
        hash = '%s:%s' % (prec, name)
        pipe.zadd('known:', {hash: 0})
        pipe.hincrby('count: ' + hash, pnow, count)
    pipe.execute()


def get_counter(conn, name, precision):
    """
    get_counter
    @param conn:
    @param name:
    @param precision:
    @return:
    """
    hash = "%s:%s" % (precision, name)
    data = conn.hgetall('count:' + hash)
    to_return = []

    for key, value in data.items():
        to_return.append((int(key), int(value)))
    to_return.sort()

    return to_return


def clean_counters(conn):
    """
    clean_counters
    @param conn:
    @return:
    """
    pipe = conn.pipeline(True)
    passes = 0

    while not QUIT:
        start = time.time()
        index = 0
        while index < conn.zcard('known:'):
            hash = conn.zcard('known:', index, index)
            index += 1
            if not hash:
                break

            hash = hash[0]
            prec = int(hash.partition(b':')[0])
            bprec = int(prec // 60) or 1
            if passes % bprec:
                continue

            hkey = 'count:' + to_str(hash)
            cutoff = time.time() - SAMPLE_COUNT * prec
            samples = list(map(int, conn.hkeys(hkey)))
            samples.sort()
            remove = bisect.bisect_right(samples, cutoff)

            if remove:
                conn.hdel(hkey, *samples[:remove])
                if remove == len(samples):
                    try:
                        pipe.watch(hkey)
                        if not pipe.hlen(hkey):
                            pipe.multi()
                            pipe.zrem('known:', hash)
                            pipe.execute()
                            index -= 1
                        else:
                            pipe.unwatch()
                    except redis.exceptions.WatchError:
                        pass

        passes += 1
        duration = min(int(time.time() - start) + 1, 60)
        time.sleep(max(60 - duration, 1))


def update_stats(conn, context, type, value, timeout=5):
    """
    update_stats
    @param conn:
    @param context:
    @param type:
    @param value:
    @param timeout:
    @return:
    """
    destination = 'stats:%s:%s' % (context, type)
    start_key = destination + ':start'
    pipe = conn.pipeline(True)
    end = time.time() + timeout

    while time.time() < end:
        try:
            pipe.watch(start_key)
            now = datetime.utcnow().timetuple()
            hour_start = datetime(*now[:4]).isoformat()

            existing = pipe.get(start_key)
            pipe.multi()

            if not existing:
                pipe.set(start_key, hour_start)
            elif to_str(existing) < hour_start:
                pipe.rename(destination, destination + ':last')
                pipe.rename(start_key, destination + ':pstart')
                pipe.set(start_key, hour_start)

            tkey1 = str(uuid.uuid4())
            tkey2 = str(uuid.uuid4())
            pipe.zadd(tkey1, {'min': value})
            pipe.zadd(tkey1, {'max': value})
            pipe.zunionstore(destination, [destination, tkey1], aggregate='min')
            pipe.zunionstore(destination, [destination, tkey2], aggregate='max')

            pipe.delete(tkey1, tkey2)
            pipe.zincrby(destination, 1, 'count')
            pipe.zincrby(destination, value, 'sum')
            pipe.zincrby(destination, value * value, 'sumsq')

            return pipe.execute()[-3:]
        except redis.exceptions.WatchError:
            continue


def get_stats(conn, context, type):
    """
    get_stats
    @param conn:
    @param context:
    @param type:
    @return:
    """
    key = 'stats:%s:%s' % (context, type)
    data = dict(conn.zrange(key, 0, -1, withscores=True))
    data[b'average'] = data[b'sum'] / data[b'count']
    numerator = data[b'sumsq'] - data[b'sum'] ** 2 / data[b'count']
    data[b'stddev'] = (numerator / (data[b'count'] - 1 or 1)) ** 0.5

    return data


@contextlib.contextmanager
def access_time(conn, context):
    """
    access_time
    @param conn:
    @param context:
    @return:
    """
    start = time.time()
    yield

    delta = time.time() - start
    stats = update_stats(conn, context, 'AccessTime', delta)
    average = stats[1] / stats[0]

    pipe = conn.pipeline(True)
    pipe.zadd('slowest:AccessTime', {context: average})
    pipe.zremrangebyrank('slowest:AccessTime', 0, -101)
    pipe.execute()


def process_view(conn, callback):
    """
    process_view
    @param conn:
    @param callback:
    @return:
    """
    with access_time(conn, request.path):
        return callback()


def ip_to_score(ip_address):
    """
    ip_to_score
    @param ip_address:
    @return:
    """
    score = 0
    for v in ip_address.split('.'):
        score = score * 256 + int(v, 10)

    return score


def import_ips_to_redis(conn, filename):
    """
    import_ips_to_redis
    @param conn:
    @param filename:
    @return:
    """
    csv_file = csv.reader(open(filename, 'rb'))
    for count, row in enumerate(csv_file):
        start_ip = row[0] if row else ''
        if 'i' in start_ip.lower():
            continue
        if '.' in start_ip:
            start_ip = ip_to_score(start_ip)
        elif start_ip.isdigit():
            start_ip = int(start_ip, 10)
        else:
            continue

        city_id = row[2] + '_' + str(count)
        conn.zadd('ip2cityid:', {city_id: start_ip})


def import_cities_to_redis(conn, filename):
    """
    import_cities_to_redis
    @param conn:
    @param filename:
    @return:
    """
    for row in csv.reader(open(filename, 'rb')):
        if len(row) < 4 or row[0].isdigit():
            continue
        row = [i.decode('latin-1') for i in row]
        city_id = row[0]
        country = row[1]
        region = row[2]
        city = row[3]
        conn.hset('cityid2city:', city_id, json.dumps([city, country, region]))


def find_city_by_ip(conn, ip_address):
    """
    find_city_by_ip
    @param conn:
    @param ip_address:
    @return:
    """
    if isinstance(ip_address, str):
        ip_address = ip_to_score(ip_address)

    city_id = conn.zrevrangebyscore('ip2cityid:', ip_address, 0, start=0, num=1)

    if not city_id:
        return None

    city_id = city_id[0].partition('_')[0]

    return json.loads(conn.hget('cityid2city:', city_id))


def is_under_maintenance(conn):
    """
    is_under_maintenance
    @param conn:
    @return:
    """
    global LAST_CHECKED, IS_UNDER_MAINTENANCE

    if (not LAST_CHECKED) or LAST_CHECKED < time.time() - 1:
        LAST_CHECKED = time.time()
        IS_UNDER_MAINTENANCE = bool(conn.get('is-under-maintenance'))

    return IS_UNDER_MAINTENANCE


def set_config(conn, type, component, config):
    """
    set_config
    @param conn:
    @param type:
    @param component:
    @param config:
    @return:
    """
    conn.set('config:%s:%s' % (type, component), json.dumps(config))


def get_config(conn, type, component, wait=1):
    """
    get_config
    @param conn:
    @param type:
    @param component:
    @param wait:
    @return:
    """
    key = 'config:%s:%s' % (type, component)

    ch = CHECKED.get(key)
    if (not ch) or ch < time.time() - wait:
        CHECKED[key] = time.time()
        config = json.loads(conn.get(key) or '{}')
        config = dict((str(k), config[k]) for k in config)
        old_config = CONFIGS.get(key)

        if config != old_config:
            CONFIGS[key] = config

    return CONFIGS.get(key)


def redis_connection(component, wait=1):
    """
    redis_connection
    @param component:
    @param wait:
    @return:
    """
    key = 'config:redis:' + component

    def wrapper(function):
        @functools.wraps(function)
        def call(*args, **kwargs):
            old_config = CONFIGS.get(key, object())
            config = get_config(config_connection, 'redis', component, wait)

            if config != old_config:
                REDIS_CONNECTIONS[key] = redis.Redis(**config)

            return function(REDIS_CONNECTIONS.get(key), *args, **kwargs)

        return call

    return wrapper


# --------------- Below this line are helpers to test the code ----------------

class request:
    pass


# # a faster version with pipelines for actual testing
# def import_ips_to_redis(conn, filename):
#     csv_file = csv.reader(open(filename, 'rb'))
#     pipe = conn.pipeline(False)
#     for count, row in enumerate(csv_file):
#         start_ip = row[0] if row else ''
#         if 'i' in start_ip.lower():
#             continue
#         if '.' in start_ip:
#             start_ip = ip_to_score(start_ip)
#         elif start_ip.isdigit():
#             start_ip = int(start_ip, 10)
#         else:
#             continue
#
#         city_id = row[2] + '_' + str(count)
#         pipe.zadd('ip2cityid:', {city_id: start_ip})
#         if not (count + 1) % 1000:
#             pipe.execute()
#     pipe.execute()
#
#
# def import_cities_to_redis(conn, filename):
#     pipe = conn.pipeline(False)
#     for count, row in enumerate(csv.reader(open(filename, 'rb'))):
#         if len(row) < 4 or not row[0].isdigit():
#             continue
#         row = [i.decode('latin-1') for i in row]
#         city_id = row[0]
#         country = row[1]
#         region = row[2]
#         city = row[3]
#         pipe.hset('cityid2city:', city_id,
#                   json.dumps([city, region, country]))
#         if not (count + 1) % 1000:
#             pipe.execute()
#     pipe.execute()


class TestCh05(unittest.TestCase):
    def setUp(self):
        global config_connection
        import redis
        self.conn = config_connection = redis.Redis(db=15, password='123456')
        self.conn.flushdb()

    def tearDown(self):
        self.conn.flushdb()
        del self.conn
        global config_connection, QUIT, SAMPLE_COUNT
        config_connection = None
        QUIT = False
        SAMPLE_COUNT = 100
        print()
        print()

    def test_log_recent(self):
        import pprint
        conn = self.conn

        print("Let's write a few logs to the recent log")
        for msg in range(5):
            log_recent(conn, 'test', 'this is message %s' % msg)
        recent = conn.lrange('recent:test:info', 0, -1)
        print("The current recent message log has this many messages:", len(recent))
        print("Those messages include:")
        pprint.pprint(recent[:10])
        self.assertTrue(len(recent) >= 5)

    def test_log_common(self):
        import pprint
        conn = self.conn

        print("Let's write some items to the common log")
        for count in range(1, 6):
            for i in range(count):
                log_common(conn, 'test', "message-%s" % count)
        common = conn.zrevrange('common:test:info', 0, -1, withscores=True)
        print("The current number of common messages is:", len(common))
        print("Those common messages are:")
        pprint.pprint(common)
        self.assertTrue(len(common) >= 5)

    def test_counters(self):
        import pprint
        global QUIT, SAMPLE_COUNT
        conn = self.conn

        print("Let's update some counters for now and a little in the future")
        now = time.time()
        for delta in range(10):
            update_counter(conn, 'test', count=random.randrange(1, 5), now=now + delta)
        counter = get_counter(conn, 'test', 1)
        print("We have some per-second counters:", len(counter))
        self.assertTrue(len(counter) >= 10)
        counter = get_counter(conn, 'test', 5)
        print("We have some per-5-second counters:", len(counter))
        print("These counters include:")
        pprint.pprint(counter[:10])
        self.assertTrue(len(counter) >= 2)
        print()

        tt = time.time

        def new_tt():
            return tt() + 2 * 86400

        time.time = new_tt

        print("Let's clean out some counters by setting our sample count to 0")
        SAMPLE_COUNT = 0
        t = threading.Thread(target=clean_counters, args=(conn,))
        t.setDaemon(1)  # to make sure it dies if we ctrl+C quit
        t.start()
        time.sleep(1)
        QUIT = True
        time.time = tt
        counter = get_counter(conn, 'test', 86400)
        print("Did we clean out all of the counters?", not counter)
        self.assertFalse(counter)

    def test_stats(self):
        import pprint
        conn = self.conn

        print("Let's add some data for our statistics!")
        for i in range(5):
            r = update_stats(conn, 'temp', 'example', random.randrange(5, 15))
        print("We have some aggregate statistics:", r)
        rr = get_stats(conn, 'temp', 'example')
        print("Which we can also fetch manually:")
        pprint.pprint(rr)
        self.assertTrue(rr[b'count'] >= 5)

    def test_access_time(self):
        import pprint
        conn = self.conn

        print("Let's calculate some access times...")
        for i in range(10):
            with access_time(conn, "req-%s" % i):
                time.sleep(.5 + random.random())
        print("The slowest access times are:")
        atimes = conn.zrevrange('slowest:AccessTime', 0, -1, withscores=True)
        pprint.pprint(atimes[:10])
        self.assertTrue(len(atimes) >= 10)
        print()

        def cb():
            time.sleep(1 + random.random())

        print("Let's use the callback version...")
        for i in range(5):
            request.path = 'cbreq-%s' % i
            process_view(conn, cb)
        print("The slowest access times are:")
        atimes = conn.zrevrange('slowest:AccessTime', 0, -1, withscores=True)
        pprint.pprint(atimes[:10])
        self.assertTrue(len(atimes) >= 10)

    def test_ip_lookup(self):
        conn = self.conn

        try:
            open('GeoLiteCity-Blocks.csv', 'rb')
            open('GeoLiteCity-Location.csv', 'rb')
        except:
            print("********")
            print("You do not have the GeoLiteCity database available, aborting test")
            print("Please have the following two files in the current path:")
            print("GeoLiteCity-Blocks.csv")
            print("GeoLiteCity-Location.csv")
            print("********")
            return

        print("Importing IP addresses to Redis... (this may take a while)")
        import_ips_to_redis(conn, 'GeoLiteCity-Blocks.csv')
        ranges = conn.zcard('ip2cityid:')
        print("Loaded ranges into Redis:", ranges)
        self.assertTrue(ranges > 1000)
        print()

        print("Importing Location lookups to Redis... (this may take a while)")
        import_cities_to_redis(conn, 'GeoLiteCity-Location.csv')
        cities = conn.hlen('cityid2city:')
        print("Loaded city lookups into Redis:", cities)
        self.assertTrue(cities > 1000)
        print()

        print("Let's lookup some locations!")
        rr = random.randrange
        for i in range(5):
            print(find_city_by_ip(conn, '%s.%s.%s.%s' % (rr(1, 255), rr(256), rr(256), rr(256))))

    def test_is_under_maintenance(self):
        print("Are we under maintenance (we shouldn't be)?", is_under_maintenance(self.conn))
        self.conn.set('is-under-maintenance', 'yes')
        print("We cached this, so it should be the same:", is_under_maintenance(self.conn))
        time.sleep(1)
        print("But after a sleep, it should change:", is_under_maintenance(self.conn))
        print("Cleaning up...")
        self.conn.delete('is-under-maintenance')
        time.sleep(1)
        print("Should be False again:", is_under_maintenance(self.conn))

    def test_config(self):
        print("Let's set a config and then get a connection from that config...")
        set_config(self.conn, 'redis', 'test', {'db': 15})

        @redis_connection('test')
        def test(conn2):
            return bool(conn2.info())

        print("We can run commands from the configured connection:", test())


if __name__ == '__main__':
    unittest.main()
