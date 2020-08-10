"""
@author: magician
@file:   coroutine_demo.py
@date:   2020/8/10
"""
from collections import namedtuple


def my_coroutine():
    """
    my_coroutine
    @return:
    """
    while True:
        received = yield
        print('Received:', received)


def minimize():
    """
    minimize
    @return:
    """
    current = yield
    while True:
        value = yield current
        current = min(value, current)


ALIVE = '*'
EMPTY = '-'

Query = namedtuple('Query', ('y', 'x'))
Transition = namedtuple('Transition', ('y', 'x', 'state'))
TICK = object()


def count_neighbors(y, x):
    """
    count_neighbors
    @param y:
    @param x:
    @return:
    """
    n_ = yield Query(y + 1, x + 0)  # North
    ne = yield Query(y + 1, x + 1)  # Northeast
    e_ = yield Query(y, x + 1)  # Northeast
    se = yield Query(y - 1, x + 1)  # Northeast
    s_ = yield Query(y - 1, x)  # Northeast
    sw = yield Query(y - 1, x - 1)  # Northeast
    w_ = yield Query(y, x - 1)  # Northeast
    nw = yield Query(y + 1, x - 1)  # Northeast
    neighbors_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0

    for state in neighbors_states:
        if state == ALIVE:
            count += 1

    return count


def game_logic(state, neighbors):
    """
    game_logic
    @param state:
    @param neighbors:
    @return:
    """
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE

    return state


def step_cell(y, x):
    """
    step_cell
    @param y:
    @param x:
    @return:
    """
    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)


def simulate(height, width):
    """
    simulate
    @param height:
    @param width:
    @return:
    """
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y, x)
        yield TICK


class Grid(object):
    """
    Grid
    """

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def __str__(self):
        for row in self.rows:
            print(row)

    def query(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def assign(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state


def live_a_generation(grid, sim):
    """
    live_a_generation
    @param grid:
    @param sim:
    @return:
    """
    progeny = Grid(grid.height, grid.width)
    item = next(sim)
    while item is not TICK:
        if isinstance(item, Query):
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)

    return progeny


class ColumnPrinter(object):
    """
    ColumnPrinter
    """

    def __init__(self):
        self.printer = []

    def append(self, param):
        self.printer.append(param)


if __name__ == '__main__':
    it = my_coroutine()
    next(it)  # Prime the coroutine
    it.send('First')
    it.send('Second')

    it1 = minimize()
    next(it1)  # Prime the generator
    print(it1.send(10))
    print(it1.send(4))
    print(it1.send(22))
    print(it1.send(-1))

    it2 = count_neighbors(10, 5)
    q1 = next(it2)
    print('First yield: ', q1)
    q2 = it2.send(ALIVE)
    print('Second yield: ', q2)
    q3 = it2.send(ALIVE)
    print('Third yield: ', q3)
    try:
        count = it2.send(EMPTY)
    except StopIteration as e:
        print('Count: ', e.value)

    it3 = step_cell(10, 5)
    q0 = next(it3)
    print('Me: ', q0)
    q1 = it.send(ALIVE)
    print('Q1: ', q1)
    t1 = it3.send(EMPTY)
    print('Outcome: ', t1)

    grid = Grid(5, 9)
    grid.assign(0, 3, ALIVE)
    print(grid)

    columns = ColumnPrinter()
    sim = simulate(grid.height, grid.width)
    for i in range(5):
        columns.append(str(grid))
        grid = live_a_generation(grid, sim)
    print(columns)
