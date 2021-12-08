"""
@author: magician
@file:   redis_action_ch07.py
@date:   2021/12/6
"""
import re
import unittest
import uuid

import math
import redis

AVERAGE_PER_1K = {}

STOP_WORDS = set('''able about across after all almost also am among
an and any are as at be because been but by can cannot could dear did
do does either else ever every for from get got had has have he her
hers him his how however if in into is it its just least let like
likely may me might most must my neither no nor not of off often on
only or other our own rather said say says she should since so some
than that the their them then there these they this tis to too twas us
wants was we were what when where which while who whom why will with
would yet you your'''.split())

WORDS_RE = re.compile("[a-z']{2,}")
QUERY_RE = re.compile("[+-]?[a-z']{2,}")


def tokenize(content):
    """
    tokenize
    @param content:
    @return:
    """
    words = set()
    for match in WORDS_RE.finditer(content.lower()):
        word = match.group().strip("'")
        if len(word) >= 2:
            words.add(word)

    return words - STOP_WORDS


def index_document(conn, docid, content):
    """
    index_document
    @param conn:
    @param docid:
    @param content:
    @return:
    """
    words = tokenize(content)

    pipeline = conn.pipeline(True)
    for word in words:
        pipeline.sadd('idx:' + word, docid)

    return len(pipeline.execute())


def _set_common(conn, method, names, ttl=30, execute=True):
    """
    _set_common
    @param conn:
    @param method:
    @param names:
    @param ttl:
    @param execute:
    @return:
    """
    id = str(uuid.uuid4())
    pipeline = conn.pipeline(True) if execute else conn
    names = ['idx:' + name for name in names]
    getattr(pipeline, method)('idx:' + id, *names)
    pipeline.expire('idx:' + id, ttl)
    if execute:
        pipeline.execute()

    return id


def intersect(conn, items, ttl=30, _execute=True):
    """
    intersect
    @param conn:
    @param items:
    @param ttl:
    @param _execute:
    @return:
    """
    return _set_common(conn, 'sinterstore', items, ttl, _execute)


def union(conn, items, ttl=30, _execute=True):
    """
    union
    @param conn:
    @param items:
    @param ttl:
    @param _execute:
    @return:
    """
    return _set_common(conn, 'sunionstore', items, ttl, _execute)


def difference(conn, items, ttl=30, _execute=True):
    """
    difference
    @param conn:
    @param items:
    @param ttl:
    @param _execute:
    @return:
    """
    return _set_common(conn, 'sdiffstore', items, ttl, _execute)


def parse(query):
    """
    parse
    @param query:
    @return:
    """
    unwanted = set()
    all = []
    current = set()

    for match in QUERY_RE.finditer(query.lower()):
        word = match.group()
        prefix = word[:1]
        if prefix in '+-':
            word = word[1:]
        else:
            prefix = None

        word = word.strip("'")
        if len(word) < 2 or word in STOP_WORDS:
            continue

        if prefix == '-':
            unwanted.add(word)
            continue

        if current and not prefix:
            all.append(list(current))
            current = set()
        current.add(word)

    if current:
        all.append(list(current))

    return all, list(unwanted)


def parse_and_search(conn, query, ttl=30):
    """
    parse_and_search
    @param conn:
    @param query:
    @param ttl:
    @return:
    """
    all, unwanted = parse(query)
    if not all:
        return None

    to_intersect = []
    for syn in all:
        if len(syn) > 1:
            to_intersect.append(union(conn, syn, ttl=ttl))
        else:
            to_intersect.append(syn[0])

    if len(to_intersect) > 1:
        intersect_result = intersect(conn, to_intersect, ttl=ttl)
    else:
        intersect_result = to_intersect[0]

    if unwanted:
        unwanted.insert(0, intersect_result)
        return difference(conn, unwanted, ttl=ttl)

    return intersect_result


def search_and_sort(conn, query, id=None, ttl=300, sort="-updated", start=0, num=20):
    """
    search_and_sort
    @param conn:
    @param query:
    @param id:
    @param ttl:
    @param sort:
    @param start:
    @param num:
    @return:
    """
    desc = sort.startswith('-')
    sort = sort.lstrip('-')
    by = "kb:doc:*->" + sort
    alpha = sort not in ('updated', 'id', 'created')

    if id and not conn.expire(id, ttl):
        id = None

    if not id:
        id = parse_and_search(conn, query, ttl=ttl)

    pipeline = conn.pipeline(True)
    pipeline.scard('idx:' + id)
    pipeline.sort('idx:' + id, by=by, alpha=alpha, desc=desc, start=start, num=num)
    results = pipeline.execute()

    return results[0], results[1], id


def search_and_zsort(conn, query, id=None, ttl=300, update=1, vote=0, start=0, num=20, desc=True):
    """
    search_and_zsort
    @param conn:
    @param query:
    @param id:
    @param ttl:
    @param update:
    @param vote:
    @param start:
    @param num:
    @param desc:
    @return:
    """
    if id and not conn.expire(id, ttl):
        id = None

    if not id:
        id = parse_and_search(conn, query, ttl=ttl)

        scored_search = {
            id: 0,
            'sort:update': update,
            'sort:votes': vote,
        }

    pipeline = conn.pipeline(True)
    pipeline.zcard('idx:' + id)
    if desc:
        pipeline.zrevrange('idx:' + id, start, start + num - 1)
    else:
        pipeline.zrange('idx:' + id, start, start + num - 1)
    results = pipeline.execute()

    return results[0], results[1], id


def _zset_common(conn, method, scores, ttl=30, **kw):
    """
    _zset_common
    @param conn:
    @param method:
    @param scores:
    @param ttl:
    @param kw:
    @return:
    """
    id = str(uuid.uuid4())
    execute = kw.pop('_execute', True)
    pipeline = conn.pipeline(True) if execute else conn
    for key in list(scores.keys()):
        scores['idx:' + key] = scores.pop(key)
    getattr(pipeline, method)('idx:' + id, scores, **kw)
    pipeline.expire('idx:' + id, ttl)
    if execute:
        pipeline.execute()

    return id


def zintersect(conn, items, ttl=30, **kw):
    """
    zintersect
    @param conn:
    @param items:
    @param ttl:
    @param kw:
    @return:
    """
    return _zset_common(conn, 'zinterscore', dict(items), ttl, **kw)


def zunion(conn, items, ttl=30, **kw):
    """
    zunion
    @param conn:
    @param items:
    @param ttl:
    @param kw:
    @return:
    """
    return _zset_common(conn, 'zunion', dict(items), ttl, **kw)


def string_to_score(string, ignore_case=False):
    """
    string_to_score
    @param string:
    @param ignore_case:
    @return:
    """
    if ignore_case:
        string = string.lower()

    pieces = list(map(ord, string[:6]))
    while len(pieces) < 6:
        pieces.append(-1)

    score = 0
    for piece in pieces:
        score = score * 257 + piece + 1

    return score * 2 + (len(string) > 6)


def to_char_map(set):
    out = {}
    for pos, val in enumerate(sorted(set)):
        out[val] = pos - 1
    return out


LOWER = to_char_map({-1} | set(range(ord('a'), ord('z') + 1)))
ALPHA = to_char_map(set(LOWER) | set(range(ord('A'), ord('Z') + 1)))
LOWER_NUMERIC = to_char_map(set(LOWER) | set(range(ord('0'), ord('9') + 1)))
ALPHA_NUMERIC = to_char_map(set(LOWER_NUMERIC) | set(ALPHA))


def string_to_score_generic(string, mapping):
    length = int(52 / math.log(len(mapping), 2))

    pieces = list(map(ord, string[:length]))
    while len(pieces) < length:
        pieces.append(-1)

    score = 0
    for piece in pieces:
        value = mapping[piece]
        score = score * len(mapping) + value + 1

    return score * 2 + (len(string) > length)


def zadd_string(conn, name, *args, **kwargs):
    pieces = list(args)
    for piece in kwargs.items():
        pieces.extend(piece)

    a = {}
    for i, v in enumerate(pieces):
        if i & 1:
            a[pieces[i - 1]] = string_to_score(v)

    return conn.zadd(name, a)


def cpc_to_ecpm(views, clicks, cpc):
    return 1000. * cpc * clicks / views


def cpa_to_ecpm(views, actions, cpa):
    return 1000. * cpa * actions / views


TO_ECPM = {
    b'cpc': cpc_to_ecpm,
    b'cpa': cpa_to_ecpm,
    b'cpm': lambda *args: args[-1],
}


def index_ad(conn, id, locations, content, type, value):
    pipeline = conn.pipeline(True)
    if not isinstance(type, bytes):
        type = type.encode('latin-1')

    for location in locations:
        pipeline.sadd('idx:req:' + location, id)

    words = tokenize(content)
    for word in words:
        pipeline.zadd('idx:' + word, {id: 0})

    rvalue = TO_ECPM[type](
        1000, AVERAGE_PER_1K.get(type, 1), value)
    pipeline.hset('type:', id, type)
    pipeline.zadd('idx:ad:value:', {id: rvalue})
    pipeline.zadd('ad:base_value:', {id: value})
    pipeline.sadd('terms:' + id, *list(words))
    pipeline.execute()


def target_ads(conn, locations, content):
    pipeline = conn.pipeline(True)
    matched_ads, base_ecpm = match_location(pipeline, locations)
    words, targeted_ads = finish_scoring(
        pipeline, matched_ads, base_ecpm, content)

    pipeline.incr('ads:served:')
    pipeline.zrevrange('idx:' + targeted_ads, 0, 0)
    target_id, targeted_ad = pipeline.execute()[-2:]

    if not targeted_ad:
        return None, None

    ad_id = targeted_ad[0]
    record_targeting_result(conn, target_id, ad_id, words)

    return target_id, ad_id


def match_location(pipe, locations):
    required = ['req:' + loc for loc in locations]
    matched_ads = union(pipe, required, ttl=300, _execute=False)
    return matched_ads, zintersect(pipe,
                                   {matched_ads: 0, 'ad:value:': 1}, _execute=False)


def finish_scoring(pipe, matched, base, content):
    bonus_ecpm = {}
    words = tokenize(content)
    for word in words:
        word_bonus = zintersect(
            pipe, {matched: 0, word: 1}, _execute=False)
        bonus_ecpm[word_bonus] = 1

    if bonus_ecpm:
        minimum = zunion(
            pipe, bonus_ecpm, aggregate='MIN', _execute=False)
        maximum = zunion(
            pipe, bonus_ecpm, aggregate='MAX', _execute=False)

        return words, zunion(
            pipe, {base: 1, minimum: .5, maximum: .5}, _execute=False)
    return words, base


def record_targeting_result(conn, target_id, ad_id, words):
    pipeline = conn.pipeline(True)

    terms = conn.smembers(b'terms:' + ad_id)
    matched = list(words & terms)
    if matched:
        matched_key = 'terms:matched:%s' % target_id
        pipeline.sadd(matched_key, *matched)
        pipeline.expire(matched_key, 900)

    type = conn.hget('type:', ad_id)
    pipeline.incr('type:%s:views:' % type)
    for word in matched:
        pipeline.zincrby('views:%s' % ad_id, 1, word)
    pipeline.zincrby('views:%s' % ad_id, 1, '')

    if not pipeline.execute()[-1] % 100:
        update_cpms(conn, ad_id)


def record_click(conn, target_id, ad_id, action=False):
    pipeline = conn.pipeline(True)
    click_key = 'clicks:%s' % ad_id

    match_key = 'terms:matched:%s' % target_id

    type = conn.hget('type:', ad_id)
    if type == 'cpa':
        pipeline.expire(match_key, 900)
        if action:
            click_key = 'actions:%s' % ad_id

    if action and type == 'cpa':
        pipeline.incr('type:%s:actions:' % type)
    else:
        pipeline.incr('type:%s:clicks:' % type)

    matched = list(conn.smembers(match_key))
    matched.append('')
    for word in matched:
        pipeline.zincrby(click_key, 1, word)
    pipeline.execute()

    update_cpms(conn, ad_id)


def update_cpms(conn, ad_id):
    pipeline = conn.pipeline(True)
    pipeline.hget('type:', ad_id)
    pipeline.zscore('ad:base_value:', ad_id)
    pipeline.smembers(b'terms:' + ad_id)
    type, base_value, words = pipeline.execute()

    which = 'clicks'
    if type == 'cpa':
        which = 'actions'

    pipeline.get('type:%s:views:' % type)
    pipeline.get('type:%s:%s' % (type, which))
    type_views, type_clicks = pipeline.execute()
    AVERAGE_PER_1K[type] = (
            1000. * int(type_clicks or '1') / int(type_views or '1'))

    if type == 'cpm':
        return

    view_key = 'views:%s' % ad_id
    click_key = '%s:%s' % (which, ad_id)

    to_ecpm = TO_ECPM[type]

    pipeline.zscore(view_key, '')
    pipeline.zscore(click_key, '')
    ad_views, ad_clicks = pipeline.execute()
    if (ad_clicks or 0) < 1:
        ad_ecpm = conn.zscore('idx:ad:value:', ad_id)
    else:
        ad_ecpm = to_ecpm(ad_views or 1, ad_clicks or 0, base_value)
        pipeline.zadd('idx:ad:value:', {ad_id: ad_ecpm})

    for word in words:
        pipeline.zscore(view_key, word)
        pipeline.zscore(click_key, word)
        views, clicks = pipeline.execute()[-2:]

        if (clicks or 0) < 1:
            continue

        word_ecpm = to_ecpm(views or 1, clicks or 0, base_value)
        bonus = word_ecpm - ad_ecpm
        pipeline.zadd('idx:' + word, {ad_id: bonus})
    pipeline.execute()


def add_job(conn, job_id, required_skills):
    conn.sadd('job:' + job_id, *required_skills)


def is_qualified(conn, job_id, candidate_skills):
    temp = str(uuid.uuid4())
    pipeline = conn.pipeline(True)
    pipeline.sadd(temp, *candidate_skills)
    pipeline.expire(temp, 5)
    pipeline.sdiff('job:' + job_id, temp)
    return not pipeline.execute()[-1]


def index_job(conn, job_id, skills):
    pipeline = conn.pipeline(True)
    for skill in skills:
        pipeline.sadd('idx:skill:' + skill, job_id)
    pipeline.zadd('idx:jobs:req', {job_id: len(set(skills))})
    pipeline.execute()


def find_jobs(conn, candidate_skills):
    skills = {}
    for skill in set(candidate_skills):
        skills['skill:' + skill] = 1

    job_scores = zunion(conn, skills)
    final_result = zintersect(
        conn, {job_scores: -1, 'jobs:req': 1})

    return conn.zrangebyscore('idx:' + final_result, 0, 0)


SKILL_LEVEL_LIMIT = 2


def index_job_levels(conn, job_id, skill_levels):
    total_skills = len(set(skill for skill, level in skill_levels))
    pipeline = conn.pipeline(True)
    for skill, level in skill_levels:
        level = min(level, SKILL_LEVEL_LIMIT)
        for wlevel in range(level, SKILL_LEVEL_LIMIT + 1):
            pipeline.sadd('idx:skill:%s:%s' % (skill, wlevel), job_id)
    pipeline.zadd('idx:jobs:req', {job_id: total_skills})
    pipeline.execute()


def search_job_levels(conn, skill_levels):
    skills = {}
    for skill, level in skill_levels:
        level = min(level, SKILL_LEVEL_LIMIT)
        skills['skill:%s:%s' % (skill, level)] = 1

    job_scores = zunion(conn, skills)
    final_result = zintersect(conn, {job_scores: -1, 'jobs:req': 1})

    return conn.zrangebyscore('idx:' + final_result, '-inf', 0)


def index_job_years(conn, job_id, skill_years):
    total_skills = len(set(skill for skill, years in skill_years))
    pipeline = conn.pipeline(True)
    for skill, years in skill_years:
        pipeline.zadd(
            'idx:skill:%s:years' % skill, {job_id: max(years, 0)})
    pipeline.sadd('idx:jobs:all', job_id)
    pipeline.zadd('idx:jobs:req', {job_id: total_skills})
    pipeline.execute()


def search_job_years(conn, skill_years):
    skill_years = dict(skill_years)
    pipeline = conn.pipeline(True)

    union = []
    for skill, years in skill_years.items():
        sub_result = zintersect(pipeline,
                                {'jobs:all': -years, 'skill:%s:years' % skill: 1}, _execute=False)
        pipeline.zremrangebyscore('idx:' + sub_result, '(0', 'inf')
        union.append(
            zintersect(pipeline, {'jobs:all': 1, sub_result: 0}, _execute=False))

    job_scores = zunion(pipeline, dict((key, 1) for key in union), _execute=False)
    final_result = zintersect(pipeline, {job_scores: -1, 'jobs:req': 1}, _execute=False)

    pipeline.zrangebyscore('idx:' + final_result, '-inf', 0)
    return pipeline.execute()[-1]


class TestCh07(unittest.TestCase):
    content = 'this is some random content, look at how it is indexed.'

    def setUp(self):
        self.conn = redis.Redis(db=15, password='123456')
        self.conn.flushdb()

    def tearDown(self):
        self.conn.flushdb()

    def test_index_document(self):
        print("We're tokenizing some content...")
        tokens = tokenize(self.content)
        print("Those tokens are:", tokens)
        self.assertTrue(tokens)

        print("And now we are indexing that content...")
        r = index_document(self.conn, 'test', self.content)
        self.assertEqual(r, len(tokens))
        for t in tokens:
            self.assertEqual(self.conn.smembers('idx:' + t), {b'test'})

    def test_set_operations(self):
        index_document(self.conn, 'test', self.content)

        r = intersect(self.conn, ['content', 'indexed'])
        self.assertEqual(self.conn.smembers('idx:' + r), {b'test'})

        r = intersect(self.conn, ['content', 'ignored'])
        self.assertEqual(self.conn.smembers('idx:' + r), set())

        r = union(self.conn, ['content', 'ignored'])
        self.assertEqual(self.conn.smembers('idx:' + r), {b'test'})

        r = difference(self.conn, ['content', 'ignored'])
        self.assertEqual(self.conn.smembers('idx:' + r), {b'test'})

        r = difference(self.conn, ['content', 'indexed'])
        self.assertEqual(self.conn.smembers('idx:' + r), set())

    def test_parse_query(self):
        query = 'test query without stopwords'
        self.assertEqual(parse(query), ([[x] for x in query.split()], []))

        query = 'test +query without -stopwords'
        self.assertIn(parse(query), (([['test', 'query'], ['without']], ['stopwords'],),
                                     ([['query', 'test'], ['without']], ['stopwords'],)))

    def test_parse_and_search(self):
        print("And now we are testing search...")
        index_document(self.conn, 'test', self.content)

        r = parse_and_search(self.conn, 'content')
        self.assertEqual(self.conn.smembers('idx:' + r), {b'test'})

        r = parse_and_search(self.conn, 'content indexed random')
        self.assertEqual(self.conn.smembers('idx:' + r), {b'test'})

        r = parse_and_search(self.conn, 'content +indexed random')
        self.assertEqual(self.conn.smembers('idx:' + r), {b'test'})

        r = parse_and_search(self.conn, 'content indexed +random')
        self.assertEqual(self.conn.smembers('idx:' + r), {b'test'})

        r = parse_and_search(self.conn, 'content indexed -random')
        self.assertEqual(self.conn.smembers('idx:' + r), set())

        print("Which passed!")

    def test_search_with_sort(self):
        print("And now let's test searching with sorting...")

        index_document(self.conn, 'test', self.content)
        index_document(self.conn, 'test2', self.content)
        self.conn.hmset('kb:doc:test', {'updated': 12345, 'id': 10})
        self.conn.hmset('kb:doc:test2', {'updated': 54321, 'id': 1})

        r = search_and_sort(self.conn, "content")
        self.assertEqual(r[1], [b'test2', b'test'])

        r = search_and_sort(self.conn, "content", sort='-id')
        self.assertEqual(r[1], [b'test', b'test2'])
        print("Which passed!")

    def test_search_with_zsort(self):
        print("And now let's test searching with sorting via zset...")

        index_document(self.conn, 'test', self.content)
        index_document(self.conn, 'test2', self.content)
        self.conn.zadd('idx:sort:update', {'test': 12345, 'test2': 54321})
        self.conn.zadd('idx:sort:votes', {'test': 10, 'test2': 1})

        r = search_and_zsort(self.conn, "content", desc=False)
        self.assertEqual(r[1], [b'test', b'test2'])

        r = search_and_zsort(self.conn, "content", update=0, vote=1, desc=False)
        self.assertEqual(r[1], [b'test2', b'test'])
        print("Which passed!")

    def test_string_to_score(self):
        words = 'these are some words that will be sorted'.split()
        pairs = [(word, string_to_score(word)) for word in words]
        pairs2 = list(pairs)
        pairs.sort()
        pairs2.sort(key=lambda x: x[1])
        self.assertEqual(pairs, pairs2)

        words = 'these are some words that will be sorted'.split()
        pairs = [(word, string_to_score_generic(word, LOWER)) for word in words]
        pairs2 = list(pairs)
        pairs.sort()
        pairs2.sort(key=lambda x: x[1])
        self.assertEqual(pairs, pairs2)

        zadd_string(self.conn, 'key', 'test', 'value', test2='other')
        self.assertEqual(self.conn.zscore('key', 'test'), string_to_score('value'))
        self.assertEqual(self.conn.zscore('key', 'test2'), string_to_score('other'))

    def test_index_and_target_ads(self):
        index_ad(self.conn, '1', ['USA', 'CA'], self.content, 'cpc', .25)
        index_ad(self.conn, '2', ['USA', 'VA'], self.content + ' wooooo', 'cpc', .125)

        for i in range(100):
            ro = target_ads(self.conn, ['USA'], self.content)
        self.assertEqual(ro[1], b'1')

        r = target_ads(self.conn, ['VA'], 'wooooo')
        self.assertEqual(r[1], b'2')

        self.assertEqual(self.conn.zrange('idx:ad:value:', 0, -1, withscores=True), [(b'2', 0.125), (b'1', 0.25)])
        self.assertEqual(self.conn.zrange('ad:base_value:', 0, -1, withscores=True), [(b'2', 0.125), (b'1', 0.25)])

        record_click(self.conn, ro[0], ro[1])

        self.assertEqual(self.conn.zrange('idx:ad:value:', 0, -1, withscores=True), [(b'2', 0.125), (b'1', 2.5)])
        self.assertEqual(self.conn.zrange('ad:base_value:', 0, -1, withscores=True), [(b'2', 0.125), (b'1', 0.25)])

    def test_is_qualified_for_job(self):
        add_job(self.conn, 'test', ['q1', 'q2', 'q3'])
        self.assertTrue(is_qualified(self.conn, 'test', ['q1', 'q3', 'q2']))
        self.assertFalse(is_qualified(self.conn, 'test', ['q1', 'q2']))

    def test_index_and_find_jobs(self):
        index_job(self.conn, 'test1', ['q1', 'q2', 'q3'])
        index_job(self.conn, 'test2', ['q1', 'q3', 'q4'])
        index_job(self.conn, 'test3', ['q1', 'q3', 'q5'])

        self.assertEqual(find_jobs(self.conn, ['q1']), [])
        self.assertEqual(find_jobs(self.conn, ['q1', 'q3', 'q4']), [b'test2'])
        self.assertEqual(find_jobs(self.conn, ['q1', 'q3', 'q5']), [b'test3'])
        self.assertEqual(find_jobs(self.conn, ['q1', 'q2', 'q3', 'q4', 'q5']), [b'test1', b'test2', b'test3'])

    def test_index_and_find_jobs_levels(self):
        print("now testing find jobs with levels ...")
        index_job_levels(self.conn, "job1", [('q1', 1)])
        index_job_levels(self.conn, "job2", [('q1', 0), ('q2', 2)])

        self.assertEqual(search_job_levels(self.conn, [('q1', 0)]), [])
        self.assertEqual(search_job_levels(self.conn, [('q1', 1)]), [b'job1'])
        self.assertEqual(search_job_levels(self.conn, [('q1', 2)]), [b'job1'])
        self.assertEqual(search_job_levels(self.conn, [('q2', 1)]), [])
        self.assertEqual(search_job_levels(self.conn, [('q2', 2)]), [])
        self.assertEqual(search_job_levels(self.conn, [('q1', 0), ('q2', 1)]), [])
        self.assertEqual(search_job_levels(self.conn, [('q1', 0), ('q2', 2)]), [b'job2'])
        self.assertEqual(search_job_levels(self.conn, [('q1', 1), ('q2', 1)]), [b'job1'])
        self.assertEqual(search_job_levels(self.conn, [('q1', 1), ('q2', 2)]), [b'job1', b'job2'])
        print("which passed")

    def test_index_and_find_jobs_years(self):
        print("now testing find jobs with years ...")
        index_job_years(self.conn, "job1", [('q1', 1)])
        index_job_years(self.conn, "job2", [('q1', 0), ('q2', 2)])

        self.assertEqual(search_job_years(self.conn, [('q1', 0)]), [])
        self.assertEqual(search_job_years(self.conn, [('q1', 1)]), [b'job1'])
        self.assertEqual(search_job_years(self.conn, [('q1', 2)]), [b'job1'])
        self.assertEqual(search_job_years(self.conn, [('q2', 1)]), [])
        self.assertEqual(search_job_years(self.conn, [('q2', 2)]), [])
        self.assertEqual(search_job_years(self.conn, [('q1', 0), ('q2', 1)]), [])
        self.assertEqual(search_job_years(self.conn, [('q1', 0), ('q2', 2)]), [b'job2'])
        self.assertEqual(search_job_years(self.conn, [('q1', 1), ('q2', 1)]), [b'job1'])
        self.assertEqual(search_job_years(self.conn, [('q1', 1), ('q2', 2)]), [b'job1', b'job2'])
        print("which passed")


if __name__ == '__main__':
    unittest.main()
