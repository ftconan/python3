"""
@author: magician
@file:   redis_action_ch04.py
@date:   2021/11/22
"""
import os
import time
import unittest
import uuid

import redis


def process_logs(conn, path, callback):
    """
    process_logs
    @param conn:
    @param path:
    @param callback:
    @return:
    """
    current_file, offset = conn.mget(
        'progress:file',
        'progress:position',
    )
    pipe = conn.pipeline()

    def update_progress():
        """
        update_progress
        @return:
        """
        pipe.mset({
            'progress:file': fname,
            'progress:position': offset,
        })
        pipe.execute()

    for fname in sorted(os.listdir(path)):
        if fname < current_file:
            continue

        inp = open(os.path.join(path, fname), 'rb')
        if fname == current_file:
            inp.seek(int(offset, 10))
        else:
            offset = 0

        current_file = 0

        for lno, line in enumerate(inp):
            callback(pipe, line)
            offset = int(offset) + len(line)

            if not (lno+1) % 1000:
                update_progress()
        update_progress()

        inp.close()


def wait_for_sync(mconn, sconn):
    """
    wait_for_sync
    @param mconn:
    @param sconn:
    @return:
    """
    identifier = str(uuid.uuid4())
    mconn.zadd('sync:wait', {identifier: time.time()})

    while not sconn.info()['master_link_status'] != 'up':
        time.sleep(0.001)

    while not sconn.zscore('sync:wait', identifier):
        time.sleep(0.001)

    deadline = time.time() + 1.01
    while time.time() < deadline:
        if sconn.info()['aof_pending_bio_fsync'] == 0:
            break
        time.sleep(0.001)

    mconn.zrem('sync:wait', identifier)
    mconn.zremrangebyscore('sync:wait', 0, time.time()-900)


def list_item(conn, itemid, sellerid, price):
    """
    list_item
    @param conn:
    @param itemid:
    @param sellerid:
    @param price:
    @return:
    """
    inventory = "inventory:%s" % sellerid
    item = "%s.%s" % (itemid, sellerid)
    end = time.time() + 5
    pipe = conn.pipeline()

    while time.time() < end:
        try:
            pipe.watch(inventory)
            if not pipe.sismember(inventory, itemid):
                pipe.unwatch()
                return None

            pipe.multi()
            pipe.zadd("market:", {item: price})
            pipe.srem(inventory, itemid)
            pipe.execute()
            return True
        except redis.exceptions.WatchError:
            pass

    return False


def purchase_item(conn, buyerid, itemid, sellerid, lprice):
    """
    purchase_item
    @param conn:
    @param buyerid:
    @param itemid:
    @param sellerid:
    @param lprice:
    @return:
    """
    buyer = "users:%s" % buyerid
    seller = "users:%s" % sellerid
    item = "%s.%s" % (itemid, sellerid)
    inventory = "inventory:%s" % buyerid
    end = time.time() + 10
    pipe = conn.pipeline()

    while time.time() < end:
        try:
            pipe.watch("market:", buyer)
            price = pipe.zscore("market:", item)
            funds = int(pipe.hget(buyer, "funds"))
            if price != lprice or price > funds:
                pipe.unwatch()
                return None

            pipe.multi()
            pipe.hincrby(seller, "funds", int(price))
            pipe.hincrby(buyer, "funds", int(-price))
            pipe.sadd(inventory, itemid)
            pipe.zrem("market:", item)
            pipe.execute()
            return True
        except redis.exceptions.WatchError:
            pass

    return False


def update_token(conn, token, user, item=None):
    """
    update_token
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


def update_token_pipeline(conn, token, user, item=None):
    """
    update_token_pipeline
    @param conn:
    @param token:
    @param user:
    @param item:
    @return:
    """
    timestamp = time.time()
    pipe = conn.pipeline(False)
    pipe.hset('login:', token, user)
    pipe.zadd('recent:', {token: timestamp})

    if item:
        pipe.zadd('viewed:' + token, {item: timestamp})
        pipe.zremrangebyrank('viewed:' + token, 0, -26)
        pipe.zincrby('viewed:', -1, item)
    pipe.execute()


def benchmark_update_token(conn, duration):
    """
    benchmark_update_token
    @param conn:
    @param duration:
    @return:
    """
    for function in (update_token, update_token_pipeline):
        count = 0
        start = time.time()
        end = start + duration
        while time.time() < end:
            count += 1
            function(conn, 'token', 'user', 'item')

        delta = time.time() - start
        print(function.__name__, count, delta, count / delta)


# --------------- Below this line are helpers to test the code ----------------


class TestCh04(unittest.TestCase):
    def setUp(self):
        import redis
        self.conn = redis.Redis(db=15, password='123456')
        self.conn.flushdb()

    def tearDown(self):
        self.conn.flushdb()
        del self.conn
        print()
        print()

    # We can't test process_logs, as that would require writing to disk, which
    # we don't want to do.

    # We also can't test wait_for_sync, as we can't guarantee that there are
    # multiple Redis servers running with the proper configuration

    def test_list_item(self):
        import pprint
        conn = self.conn

        print("We need to set up just enough state so that a user can list an item")
        seller = 'userX'
        item = 'itemX'
        conn.sadd('inventory:' + seller, item)
        i = conn.smembers('inventory:' + seller)
        print("The user's inventory has:", i)
        self.assertTrue(i)
        print()

        print("Listing the item...")
        l = list_item(conn, item, seller, 10)
        print("Listing the item succeeded?", l)
        self.assertTrue(l)
        r = conn.zrange('market:', 0, -1, withscores=True)
        print("The market contains:")
        pprint.pprint(r)
        self.assertTrue(r)
        self.assertTrue(any(x[0] == b'itemX.userX' for x in r))

    def test_purchase_item(self):
        self.test_list_item()
        conn = self.conn

        print("We need to set up just enough state so a user can buy an item")
        buyer = 'userY'
        conn.hset('users:userY', 'funds', 125)
        r = conn.hgetall('users:userY')
        print("The user has some money:", r)
        self.assertTrue(r)
        self.assertTrue(r.get(b'funds'))
        print()

        print("Let's purchase an item")
        p = purchase_item(conn, 'userY', 'itemX', 'userX', 10)
        print("Purchasing an item succeeded?", p)
        self.assertTrue(p)
        r = conn.hgetall('users:userY')
        print("Their money is now:", r)
        self.assertTrue(r)
        i = conn.smembers('inventory:' + buyer)
        print("Their inventory is now:", i)
        self.assertTrue(i)
        self.assertTrue(b'itemX' in i)
        self.assertEqual(conn.zscore('market:', 'itemX.userX'), None)

    def test_benchmark_update_token(self):
        benchmark_update_token(self.conn, 5)


if __name__ == '__main__':
    unittest.main()
