"""
@author: magician
@file:   redis_action_ch06.py
@date:   2021/11/23
"""
import bisect
import json
import os
import time
import unittest
import uuid
from collections import defaultdict, deque

import math
import redis
import zlib

QUIT = False
pipe = inv = item = buyer = seller = inventory = None


def add_update_contact(conn, user, contact):
    """
    add_update_contact
    @param conn:
    @param user:
    @param contact:
    @return:
    """
    ac_list = 'recent:' + user
    pipeline = conn.pipeline(True)
    pipeline.lrem(ac_list, 1, contact)
    pipeline.lpush(ac_list, contact)
    pipeline.ltrim(ac_list, 0, 99)
    pipeline.execute()


def remove_contact(conn, user, contact):
    """
    remove_contact
    @param conn:
    @param user:
    @param contact:
    @return:
    """
    conn.lrem('recent:' + user, 1, contact)


def fetch_autocomplete_list(conn, user, prefix):
    candidates = conn.lrange('recent:' + user, 0, -1)
    matches = []
    prefix = prefix.encode()
    for candidate in candidates:
        if candidate.lower().startswith(prefix.lower()):
            matches.append(candidate)
    return matches


def fetch_autocomplete_prefix(conn, user, prefix):
    """
    fetch_autocomplete_prefix
    @param conn:
    @param user:
    @param prefix:
    @return:
    """
    candidates = conn.lrange('recent:' + user, 0, -1)
    matches = []
    prefix = prefix.decode()
    for candidate in candidates:
        if candidate.lower().startswith(prefix.lower()):
            matches.append(candidate)

    return matches


def find_prefix_range(prefix):
    """
    find_prefix_range
    @param prefix:
    @return:
    """
    valid_characters = '`abcdefghijklmnopqrstuvwxyz{'

    posn = bisect.bisect_left(valid_characters, prefix[-1:])
    suffix = valid_characters[(posn or 1) - 1]

    return prefix[:-1] + suffix + '{', prefix + '{'


def autocomplete_on_prefix(conn, guild, prefix):
    """
    autocomplete_on_prefix
    @param conn:
    @param guild:
    @param prefix:
    @return:
    """
    start, end = find_prefix_range(prefix)
    identifier = str(uuid.uuid4())
    start += identifier
    end += identifier
    zset_name = 'members:' + guild

    conn.zadd(zset_name, {'start': 0, 'end': 0})
    pipeline = conn.pipeline(True)

    while True:
        try:
            pipeline.watch(zset_name)
            sindex = pipeline.zrank(zset_name, start)
            eindex = pipeline.zrank(zset_name, end)
            erange = min(sindex + 9, eindex - 2)
            pipeline.multi()
            pipeline.zrem(zset_name, start, end)
            pipeline.zrange(zset_name, sindex, erange)
            items = pipeline.execute()[-1]
            break
        except redis.exceptions.WatchError:
            continue

    return [item for item in items if b'{' not in item]


def join_guild(conn, guild, user):
    """
    join_guild
    @param conn:
    @param guild:
    @param user:
    @return:
    """
    conn.zadd('members:' + guild, {user: 0})


def leave_guild(conn, guild, user):
    """
    leave_guild
    @param conn:
    @param guild:
    @param user:
    @return:
    """
    conn.zrem('members:' + guild, user)


def acquire_lock(conn, lockname, acquire_timeout=10.0):
    """
    acquire_lock
    @param conn:
    @param lockname:
    @param acquire_timeout:
    @return:
    """
    identifier = str(uuid.uuid4())

    end = time.time() + acquire_timeout
    while time.time() < end:
        if conn.setnx('lock:' + lockname, identifier):
            return identifier

        time.sleep(0.001)

    return False


def purchase_item_with_lock(conn, buyerid, itemid, sellerid):
    """
    purchase_item_with_lock
    @param conn:
    @param buyerid:
    @param itemid:
    @param sellerid:
    @return:
    """
    buyer = "user:%s" % buyerid
    seller = "user:%s" % sellerid
    item = "%s.%s" % (itemid, sellerid)
    inventory = "inventory:%s" % buyerid

    locked = acquire_lock(conn, 'market:')
    if not locked:
        return False

    pipe = conn.pipeline(True)
    try:
        pipe.zscore("market:", item)
        pipe.hget(buyer, 'funds')
        price, funds = pipe.execute()
        if price is None or price < funds:
            return None

        pipe.hincrby(seller, 'funds', int(price))
        pipe.hincrby(buyer, 'funds', int(-price))
        pipe.sadd(inventory, itemid)
        pipe.zrem("market:", item)
        pipe.execute()

        return True
    finally:
        release_lock(conn, 'market:', locked)


def release_lock(conn, lockname, identifier):
    """
    release_lock
    @param conn:
    @param lockname:
    @param identifier:
    @return:
    """
    pipe = conn.pipeline(True)
    lockname = "lock:" + identifier
    if isinstance(identifier, str):
        identifier = identifier.encode()

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


def acquire_lock_with_timeout(conn, lockname, acquire_timeout=10, lock_timeout=10):
    """
    acquire_lock_with_timeout
    @param conn:
    @param lockname:
    @param acquire_timeout:
    @param lock_timeout:
    @return:
    """
    identifier = str(uuid.uuid4())
    lockname = 'lock:' + lockname
    lock_timeout = int(math.ceil(lock_timeout))

    end = time.time() + acquire_timeout
    while time.time() < end:
        if conn.setnx(lockname, identifier):
            conn.expire(lockname, lock_timeout)
        elif conn.ttl(lockname) < 0:
            conn.expire(lockname, lock_timeout)

        time.sleep(0.001)

    return False


def acquire_semaphore(conn, semname, limit, timeout=10):
    """
    acquire_semaphore
    @param conn:
    @param semname:
    @param limit:
    @param timeout:
    @return:
    """
    identifier = str(uuid.uuid4())
    now = time.time()

    pipeline = conn.pipeline(True)
    pipeline.zremrangebyscore(semname, '-inf', now - timeout)
    pipeline.zadd(semname, {identifier: now})
    pipeline.zrank(semname, identifier)
    if pipeline.execute()[-1] < limit:
        return identifier

    conn.zrem(semname, identifier)

    return None


def release_semaphore(conn, semname, identifier):
    """
    release_semaphore
    @param conn:
    @param semname:
    @param identifier:
    @return:
    """
    return conn.zrem(semname, identifier)


def acquire_fair_semaphore(conn, semname, limit, timeout=10):
    """
    acquire_fair_semaphore
    @param conn:
    @param semname:
    @param limit:
    @param timeout:
    @return:
    """
    identifier = str(uuid.uuid4())
    czset = semname + ':owner'
    ctr = semname + ':counter'

    now = time.time()
    pipeline = conn.pipeline(True)
    pipeline.zremrangebyscore(semname, '-inf', now - timeout)
    pipeline.zinterstore(czset, {czset: 1, semname: 1})

    pipeline.incr(ctr)
    counter = pipeline.execute()[-1]

    pipeline.zadd(semname, {identifier: now})
    pipeline.zadd(czset, {identifier: counter})

    pipeline.zrank(czset, identifier)
    if pipeline.execute()[-1] < limit:
        return identifier

    pipeline.zrem(semname, identifier)
    pipeline.zrem(czset, identifier)
    pipeline.execute()

    return None


def release_fair_semaphore(conn, semname, identifier):
    """
    release_fair_semaphore
    @param conn:
    @param semname:
    @param identifier:
    @return:
    """
    pipeline = conn.pipeline(True)
    pipeline.zrem(semname, identifier)
    pipeline.zrem(semname + ':owner', identifier)

    return pipeline.execute()[0]


def refresh_fair_semaphore(conn, semname, identifier):
    """
    refresh_fair_semaphore
    @param conn:
    @param semname:
    @param identifier:
    @return:
    """
    if conn.zadd(semname, {identifier: time.time()}):
        release_fair_semaphore(conn, semname, identifier)
        return False

    return True


def acquire_semaphore_with_lock(conn, semname, limit, timeout=10):
    """
    acquire_semaphore_with_lock
    @param conn:
    @param semname:
    @param limit:
    @param timeout:
    @return:
    """
    identifier = acquire_lock(conn, semname, acquire_timeout=0.01)
    if identifier:
        try:
            return acquire_fair_semaphore(conn, semname, limit, timeout)
        finally:
            release_lock(conn, semname, identifier)


def send_sold_email_via_queue(conn, seller, item, price, buyer):
    """
    send_sold_email_via_queue
    @param conn:
    @param seller:
    @param item:
    @param price:
    @param buyer:
    @return:
    """
    data = {
        'seller': seller,
        'item': item,
        'price': price,
        'buyer': buyer,
        'time': time.time(),
    }
    conn.rpush('queue:email', json.dumps(data))


def log_error(param, err, to_send):
    print(f'param:{str(param)}, err:{str(err)}, to_send:{str(to_send)}')


def log_success(param, to_send):
    print(f'param:{str(param)}, to_send:{str(to_send)}')


def process_sold_email_queue(conn):
    """
    process_sold_email_queue
    @param conn:
    @return:
    """
    while not QUIT:
        packed = conn.blop(['queue:email', 30])
        if not packed:
            continue

        to_send = json.loads(packed[1])
        try:
            pass
        except Exception as err:
            log_error('Failed to send sold email', err, to_send)
        else:
            log_success('Sent sold email', to_send)


def worker_watch_queue(conn, queue, callbacks):
    """
    worker_watch_queue
    @param conn:
    @param queue:
    @param callbacks:
    @return:
    """
    while not QUIT:
        packed = conn.blop(['queue:email', 30])
        if not packed:
            continue

        name, args = json.loads(packed[1])
        if name not in callbacks:
            log_error("Unknown callback %s" % name)
            continue

        callbacks(name)(*args)


def worker_watch_queues(conn, queues, callbacks):
    """
    worker_watch_queues
    @param conn:
    @param queues:
    @param callbacks:
    @return:
    """
    while not QUIT:
        packed = conn.blop([queues, 30])
        if not packed:
            continue

        name, args = json.loads(packed[1])
        if name not in callbacks:
            log_error("Unknown callback %s" % name)
            continue

        callbacks(name)(*args)


def execute_later(conn, queue, name, args, delay=0):
    """
    execute_later
    @param conn:
    @param queue:
    @param name:
    @param args:
    @param delay:
    @return:
    """
    identifier = str(uuid.uuid4())
    item = json.dumps([identifier, queue, name, args])
    if delay > 0:
        conn.zadd('delayed:', {item: time.time() + delay})
    else:
        conn.rpush('queue:' + queue, item)

    return identifier


def poll_queue(conn):
    """
    poll_queue
    @param conn:
    @return:
    """
    while not QUIT:
        item = conn.zrange('delayed:', 0, 0, withscores=True)
        if not item or item[0][1] > time.time():
            time.sleep(0.01)
            continue

        item = item[0][0]
        identifier, queue, function, args = json.loads(item)

        locked = acquire_lock(conn, identifier)
        if not locked:
            continue

        if conn.zrem('delayed:', item):
            conn.rpush('queue:' + queue, item)

        release_lock(conn, identifier, locked)


def create_chat(conn, sender, recipients, message, chat_id=None):
    """
    create_chat
    @param conn:
    @param sender:
    @param recipients:
    @param message:
    @param chat_id:
    @return:
    """
    chat_id = chat_id or str(conn.incr('ids:chat_id:'))

    recipients.append(sender)
    recipientsd = dict((r, 0) for r in recipients)

    pipeline = conn.pipeline(True)
    pipeline.zadd('chat:' + chat_id, recipientsd)
    for rec in recipients:
        pipeline.zadd('seen:' + rec, {chat_id: 0})
    pipeline.execute()

    return send_message(conn, chat_id, sender, message)


def send_message(conn, chat_id, sender, message):
    identifier = acquire_lock(conn, 'chat:' + chat_id)
    if not identifier:
        raise Exception("Couldn't get the lock")
    try:
        mid = conn.incr('ids:' + chat_id)
        ts = time.time()
        packed = json.dumps({
            'id': mid,
            'ts': ts,
            'sender': sender,
            'message': message,
        })

        conn.zadd('msgs:' + chat_id, {packed: mid})
    finally:
        release_lock(conn, 'chat:' + chat_id, identifier)
    return chat_id


def fetch_pending_messages(conn, recipient):
    """
    fetch_pending_messages
    @param conn:
    @param recipient:
    @return:
    """
    seen = conn.zrange('seen:' + recipient, 0, -1, withscores=True)

    pipeline = conn.pipeline(True)

    for chat_id, seen_id in seen:
        pipeline.zrangebyscore(b'msgs:' + chat_id, seen_id + 1, 'inf')
    chat_info = list(zip(seen, pipeline.execute()))

    for i, ((chat_id, seen_id), messages) in enumerate(chat_info):
        if not messages:
            continue

        messages[:] = list(map(json.loads, messages))
        seen_id = messages[-1]['id']
        conn.zadd(b'chat:' + chat_id, {recipient: seen_id})

        min_id = conn.zrange(b'chat:' + chat_id, 0, 0, withscores=True)
        pipeline.zadd('seen:' + recipient, {chat_id: seen_id})
        if min_id:
            pipeline.zremrangebyscore(b'msgs:' + chat_id, 0, min_id[0][1])
        chat_info[i] = (chat_id, messages)
    pipeline.execute()

    return chat_info


def join_chat(conn, chat_id, user):
    """
    join_chat
    @param conn:
    @param chat_id:
    @param user:
    @return:
    """
    message_id = int(conn.get('ids:' + chat_id))

    pipeline = conn.pipeline(True)
    pipeline.zadd('chat:' + chat_id, {user: message_id})
    pipeline.zadd('seen:' + user, {chat_id: message_id})
    pipeline.execute()


def leave_chat(conn, chat_id, user):
    """
    leave_chat
    @param conn:
    @param chat_id:
    @param user:
    @return:
    """
    pipeline = conn.pipeline(True)
    pipeline.zrem('chat:' + chat_id, user)
    pipeline.zrem('seen:' + user, chat_id)
    pipeline.zcard('chat:' + chat_id)

    if not pipeline.execute()[-1]:
        pipeline.delete('msgs:' + chat_id)
        pipeline.delete('ids:' + chat_id)
        pipeline.execute()
    else:
        oldest = conn.zrange('chat:' + chat_id, 0, 0, withscores=True)
        conn.zremrangebyscore('msgs:' + chat_id, 0, oldest[0][1])


aggregates = defaultdict(lambda: defaultdict(int))


def find_city_by_ip_local(ip):
    try:
        country = ip.split('.')[2]
    except Exception as e:
        country = ''

    return country


def daily_country_aggregate(conn, line):
    """
    daily_country_aggregate
    @param conn:
    @param line:
    @return:
    """
    if line:
        line = line.split()
        ip = line[0]
        day = line[1]
        country = find_city_by_ip_local(ip)[2]
        aggregates[day][country] += 1
        return

    for day, aggregate in list(aggregates.items()):
        conn.zadd('daily:country' + day, aggregate)
        del aggregates[day]


def copy_logs_to_redis(conn, path, channel, count=10, limit=2 ** 30, quit_when_done=True):
    """
    copy_logs_to_redis
    @param conn:
    @param path:
    @param channel:
    @param count:
    @param limit:
    @param quit_when_done:
    @return:
    """
    bytes_in_redis = 0
    waiting = deque()
    create_chat(conn, 'source', list(map(str, list(range(count)))), '', channel)
    count = str(count).encode()
    for logfile in sorted(os.listdir(path)):
        full_path = os.path.join(path, logfile)
        fsize = os.stat(full_path).st_size
        while bytes_in_redis + fsize > limit:
            cleaned = _clean(conn, channel, waiting, count)
            if cleaned:
                bytes_in_redis -= cleaned
            else:
                time.sleep(0.25)

        with open(full_path, 'rb') as inp:
            block = ' '
            while block:
                block = inp.read(2 ** 17)
                conn.append(channel + logfile, block)

        send_message(conn, channel, 'source', logfile)

        bytes_in_redis += fsize
        waiting.append((logfile, fsize))

    if quit_when_done:
        send_message(conn, channel, 'source', ':done')

    while waiting:
        cleaned = _clean(conn, channel, waiting, count)
        if cleaned:
            bytes_in_redis -= cleaned
        else:
            time.sleep(0.25)


def _clean(conn, channel, waiting, count):
    """
    _clean
    @param conn:
    @param channel:
    @param waiting:
    @param count:
    @return:
    """
    if not waiting:
        return 0
    w0 = waiting[0][0]
    if (conn.get(channel + w0 + ':done') or b'0') >= count:
        conn.delete(channel + w0, channel + w0 + ':done')
        return waiting.popleft()[1]
    return 0


def process_logs_from_redis(conn, id, callback):
    """
    process_logs_from_redis
    @param conn:
    @param id:
    @param callback:
    @return:
    """
    while True:
        fdata = fetch_pending_messages(conn, id)

        for ch, mdata in fdata:
            if isinstance(ch, bytes):
                ch = ch.decode()
            for message in mdata:
                logfile = message['message']

                if logfile == ':done':
                    return
                elif not logfile:
                    continue

                block_reader = readblocks
                if logfile.endswith('.gz'):
                    block_reader = readblocks_gz

                for line in readlines(conn, ch + logfile, block_reader):
                    callback(conn, line)
                callback(conn, None)

                conn.incr(ch + logfile + ':done')

        if not fdata:
            time.sleep(0.1)


def readlines(conn, key, rblocks):
    out = b''
    for block in rblocks(conn, key):
        if isinstance(block, str):
            block = block.encode()
        out += block
        posn = out.rfind(b'\n')
        if posn >= 0:
            for line in out[:posn].split(b'\n'):
                yield line + b'\n'
            out = out[posn + 1:]
        if not block:
            yield out
            break


def readblocks(conn, key, blocksize=2 ** 17):
    lb = blocksize
    pos = 0
    while lb == blocksize:
        block = conn.substr(key, pos, pos + blocksize - 1)
        yield block
        lb = len(block)
        pos += lb
    yield ''


def readblocks_gz(conn, key):
    inp = b''
    decoder = None
    for block in readblocks(conn, key, 2 ** 17):
        if not decoder:
            inp += block
            try:
                if inp[:3] != b"\x1f\x8b\x08":
                    raise IOError("invalid gzip data")
                i = 10
                flag = inp[3]
                if flag & 4:
                    i += 2 + inp[i] + 256 * inp[i + 1]
                if flag & 8:
                    i = inp.index(b'\0', i) + 1
                if flag & 16:
                    i = inp.index(b'\0', i) + 1
                if flag & 2:
                    i += 2

                if i > len(inp):
                    raise IndexError("not enough data")
            except (IndexError, ValueError):
                continue

            else:
                block = inp[i:]
                inp = None
                decoder = zlib.decompressobj(-zlib.MAX_WBITS)
                if not block:
                    continue

        if not block:
            yield decoder.flush()
            break

        yield decoder.decompress(block)


class TestCh06(unittest.TestCase):
    def setUp(self):
        import redis
        self.conn = redis.Redis(db=15, password='123456')

    def tearDown(self):
        self.conn.flushdb()
        del self.conn
        print()
        print()

    def test_add_update_contact(self):
        import pprint
        conn = self.conn
        conn.delete('recent:user')

        print("Let's add a few contacts...")
        for i in range(10):
            add_update_contact(conn, 'user', 'contact-%i-%i' % (i // 3, i))
        print("Current recently contacted contacts")
        contacts = conn.lrange('recent:user', 0, -1)
        pprint.pprint(contacts)
        self.assertTrue(len(contacts) >= 10)
        print()

        print("Let's pull one of the older ones up to the front")
        add_update_contact(conn, 'user', 'contact-1-4')
        contacts = conn.lrange('recent:user', 0, 2)
        print("New top-3 contacts:")
        pprint.pprint(contacts)
        self.assertEqual(contacts[0], b'contact-1-4')
        print()

        print("Let's remove a contact...")
        print(remove_contact(conn, 'user', 'contact-2-6'))
        contacts = conn.lrange('recent:user', 0, -1)
        print("New contacts:")
        pprint.pprint(contacts)
        self.assertTrue(len(contacts) >= 9)
        print()

        print("And let's finally autocomplete on ")
        all = conn.lrange('recent:user', 0, -1)
        contacts = fetch_autocomplete_list(conn, 'user', 'c')
        self.assertTrue(all == contacts)
        equiv = [c for c in all if c.startswith(b'contact-2-')]
        contacts = fetch_autocomplete_list(conn, 'user', 'contact-2-')
        equiv.sort()
        contacts.sort()
        self.assertEqual(equiv, contacts)
        conn.delete('recent:user')

    def test_address_book_autocomplete(self):
        self.conn.delete('members:test')
        print("the start/end range of 'abc' is:", find_prefix_range('abc'))
        print()

        print("Let's add a few people to the guild")
        for name in ['jeff', 'jenny', 'jack', 'jennifer']:
            join_guild(self.conn, 'test', name)
        print()
        print("now let's try to find users with names starting with 'je':")
        r = autocomplete_on_prefix(self.conn, 'test', 'je')
        print(r)
        self.assertTrue(len(r) == 3)
        print("jeff just left to join a different guild...")
        leave_guild(self.conn, 'test', 'jeff')
        r = autocomplete_on_prefix(self.conn, 'test', 'je')
        print(r)
        self.assertTrue(len(r) == 2)
        self.conn.delete('members:test')

    def test_distributed_locking(self):
        self.conn.delete('lock:testlock')
        print("Getting an initial lock...")
        self.assertTrue(acquire_lock_with_timeout(self.conn, 'testlock', 1, 1))
        print("Got it!")
        print("Trying to get it again without releasing the first one...")
        self.assertFalse(acquire_lock_with_timeout(self.conn, 'testlock', .01, 1))
        print("Failed to get it!")
        print()
        print("Waiting for the lock to timeout...")
        time.sleep(2)
        print("Getting the lock again...")
        r = acquire_lock_with_timeout(self.conn, 'testlock', 1, 1)
        self.assertTrue(r)
        print("Got it!")
        print("Releasing the lock...")
        self.assertTrue(release_lock(self.conn, 'testlock', r))
        print("Released it...")
        print()
        print("Acquiring it again...")
        self.assertTrue(acquire_lock_with_timeout(self.conn, 'testlock', 1, 1))
        print("Got it!")
        self.conn.delete('lock:testlock')

    def test_counting_semaphore(self):
        self.conn.delete('testsem', 'testsem:owner', 'testsem:counter')
        print("Getting 3 initial semaphores with a limit of 3...")
        for i in range(3):
            self.assertTrue(acquire_fair_semaphore(self.conn, 'testsem', 3, 1))
        print("Done!")
        print("Getting one more that should fail...")
        self.assertFalse(acquire_fair_semaphore(self.conn, 'testsem', 3, 1))
        print("Couldn't get it!")
        print()
        print("Lets's wait for some of them to time out")
        time.sleep(2)
        print("Can we get one?")
        r = acquire_fair_semaphore(self.conn, 'testsem', 3, 1)
        self.assertTrue(r)
        print("Got one!")
        print("Let's release it...")
        self.assertTrue(release_fair_semaphore(self.conn, 'testsem', r))
        print("Released!")
        print()
        print("And let's make sure we can get 3 more!")
        for i in range(3):
            self.assertTrue(acquire_fair_semaphore(self.conn, 'testsem', 3, 1))
        print("We got them!")
        self.conn.delete('testsem', 'testsem:owner', 'testsem:counter')

    def test_delayed_tasks(self):
        import threading
        self.conn.delete('queue:tqueue', 'delayed:')
        print("Let's start some regular and delayed tasks...")
        for delay in [0, .5, 0, 1.5]:
            self.assertTrue(execute_later(self.conn, 'tqueue', 'testfn', [], delay))
        r = self.conn.llen('queue:tqueue')
        print("How many non-delayed tasks are there (should be 2)?", r)
        self.assertEqual(r, 2)
        print()
        print("Let's start up a thread to bring those delayed tasks back...")
        t = threading.Thread(target=poll_queue, args=(self.conn,))
        t.setDaemon(1)
        t.start()
        print("Started.")
        print("Let's wait for those tasks to be prepared...")
        time.sleep(2)
        global QUIT
        QUIT = True
        t.join()
        r = self.conn.llen('queue:tqueue')
        print("Waiting is over, how many tasks do we have (should be 4)?", r)
        self.assertEqual(r, 4)
        self.conn.delete('queue:tqueue', 'delayed:')

    def test_multi_recipient_messaging(self):
        self.conn.delete('ids:chat:', 'msgs:1', 'ids:1', 'seen:joe', 'seen:jeff', 'seen:jenny')

        print("Let's create a new chat session with some recipients...")
        chat_id = create_chat(self.conn, 'joe', ['jeff', 'jenny'], 'message 1')
        print("Now let's send a few messages...")
        for i in range(2, 5):
            send_message(self.conn, chat_id, 'joe', 'message %s' % i)
        print()
        print("And let's get the messages that are waiting for jeff and jenny...")
        r1 = fetch_pending_messages(self.conn, 'jeff')
        r2 = fetch_pending_messages(self.conn, 'jenny')
        print("They are the same?", r1 == r2)
        self.assertEqual(r1, r2)
        print("Those messages are:")
        import pprint
        pprint.pprint(r1)
        self.conn.delete('ids:chat:', 'msgs:1', 'ids:1', 'seen:joe', 'seen:jeff', 'seen:jenny')

    def test_file_distribution(self):
        import gzip, shutil, tempfile, threading, binascii
        self.conn.delete('test:temp-1.txt', 'test:temp-2.txt', 'test:temp-3.txt', 'msgs:test:', 'seen:0', 'seen:source',
                         'ids:test:', 'chat:test:')

        dire = tempfile.mkdtemp()
        try:
            print("Creating some temporary 'log' files...")
            sizes = []
            with open(dire + '/temp-1.txt', 'wb') as f:
                f.write(b'one line\n')
                sizes.append(f.tell())
            with open(dire + '/temp-2.txt', 'wb') as f:
                f.write(10000 * b'many lines\n')
                sizes.append(f.tell())
            out = gzip.GzipFile(dire + '/temp-3.txt.gz', mode='wb')
            for i in range(10000):
                out.write(10 * ((f'random line %s\n' % (i,)).encode()))
            out.flush()
            out.close()
            sizes.append(os.stat(dire + '/temp-3.txt.gz').st_size)
            print("Done.")
            print()
            print("Starting up a thread to copy logs to redis...")
            t = threading.Thread(target=copy_logs_to_redis,
                                 args=(self.conn, dire, 'test:', 1, sum(sizes) + 1)
                                 )
            t.daemonic = 1
            t.start()

            print("Let's pause to let some logs get copied to Redis...")
            time.sleep(.25)
            print()
            print("Okay, the logs should be ready. Let's process them!")

            index = [0]
            counts = [0, 0, 0]

            def callback(conn, line):
                if line is None:
                    print("Finished with a file %s, linecount: %s" % (index[0], counts[index[0]]))
                    index[0] += 1
                elif line or line.endswith(b'\n'):
                    counts[index[0]] += 1

            print("Files should have 1, 10000, and 100000 lines")
            process_logs_from_redis(self.conn, '0', callback)
            self.assertEqual(counts, [1, 10000, 100000])

            print()
            print("Let's wait for the copy thread to finish cleaning up...")
            t.join()
            print("Done cleaning out Redis!")

        finally:
            print("Time to clean up files...")
            shutil.rmtree(dire)
            print("Cleaned out files!")
        self.conn.delete('test:temp-1.txt', 'test:temp-2.txt', 'test:temp-3.txt', 'msgs:test:', 'seen:0', 'seen:source',
                         'ids:test:', 'chat:test:')


if __name__ == '__main__':
    unittest.main()
