""" Day 24 Solutions """

from argparse import ArgumentParser
from collections import defaultdict

from aoc.y2022.utils import load_data


U = (-1, 0)
D = (1, 0)
R = (0, 1)
L = (0, -1)
N4 = [U, D, L, R]
N5 = [U, D, L, R, (0, 0)]
dir_map = {
    ">": R,
    "^": U,
    "v": D,
    "<": L,
}
OPEN = 0
WALL = 1
char_map = {
    ".": OPEN,
    "#": WALL,
}
char_map.update(dir_map)

rev_char_map = {v: k for (k, v) in char_map.items()}


def ints(x):
    return list(map(int, x))


def print_board(board, blizz_set):
    """
    Print the board
    """
    printing = True
    y = 0
    x = 0
    lines = []
    while printing and (y, x) in board:
        row = []
        while printing:
            if (y, x) in board:
                row.append(rev_char_map[board[(y, x)]])
            else:
                printing = False
            x += 1
        printing = True
        x = 0
        y += 1
        lines.append(row)

    visited = defaultdict(lambda: 0)
    for (y, x, d) in blizz_set:
        visited[y, x] += 1
        ct = visited[y, x]
        lines[y][x] = rev_char_map[d] if ct == 1 else str(ct)

    for row in lines:
        print("".join(row))


def move_storm(blizzards, r, c):
    """move them blizz"""
    new_blizzards = []
    occupied = set()
    for y, x, d in blizzards:
        y = (y + d[0]) % r
        x = (x + d[1]) % c
        new_blizzards.append((y, x, d))
        occupied.add((y, x))
    return new_blizzards, occupied


def mdist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def heur(loc, goal):
    return mdist(loc, goal)


def heur2(state, start, goal):
    """heur2"""
    stage = state[STAGE]
    loc = state[LOC]
    heur = 0
    if stage == 0:
        heur += mdist(loc, goal)
        heur += mdist(goal, start) * 2
    elif stage == 1:
        heur += mdist(loc, start)
        heur += mdist(goal, start)
    else:
        heur = mdist(loc, goal)
    return heur


TIME = 0
LOC = 1
STAGE = 2


def legal_moves(state, blizzards, occupied, r, c, start, goal):
    """calculate legal moves"""
    t = state[TIME]
    loc = state[LOC]
    if t + 1 not in blizzards:
        b, o = move_storm(blizzards[t], r, c)
        blizzards[t + 1] = b
        occupied[t + 1] = o
    else:
        b, o = blizzards[t + 1], occupied[t + 1]
    legal = []
    for move in N5:
        dest = loc[0] + move[0], loc[1] + move[1]
        if dest in [start, goal]:
            pass
        elif dest[0] < 0 or dest[1] < 0 or dest[0] >= r or dest[1] >= c:
            continue
        if not dest in o:
            legal.append((t + 1, dest))
    return legal


def legal_moves_2(state, blizzards, occupied, r, c, start, goal):
    """calculate legal moves"""
    t = state[TIME]
    loc = state[LOC]
    stage = state[STAGE]
    if t + 1 not in blizzards:
        b, o = move_storm(blizzards[t], r, c)
        blizzards[t + 1] = b
        occupied[t + 1] = o
    else:
        b, o = blizzards[t + 1], occupied[t + 1]
    legal = []
    for move in N5:
        dest = loc[0] + move[0], loc[1] + move[1]
        if dest == goal:
            if stage == 0:
                legal.append((t + 1, dest, stage + 1))
            else:
                legal.append((t + 1, dest, stage))
        elif dest == start:
            if stage == 1:
                legal.append((t + 1, dest, stage + 1))
            else:
                legal.append((t + 1, dest, stage))
        elif dest[0] < 0 or dest[1] < 0 or dest[0] >= r or dest[1] >= c:
            continue
        if not dest in o:
            legal.append((t + 1, dest, stage))
    return legal


from heapq import heappush, heappop


def solve_puzzle(b, o, start, goal, r, c):
    """solve maze"""

    blizzards = dict()
    occupied = dict()
    blizzards[0] = b
    occupied[0] = o

    open_set_hash = defaultdict(lambda: False)
    start_state = (0, start)
    open_set_hash[start_state] = True
    open_set = [
        (float("inf"), start_state),
    ]
    came_from = dict()
    g_score = defaultdict(lambda: float("inf"))
    best_goal_score = float("inf")
    while open_set:
        _, state = heappop(open_set)
        open_set_hash[state] = False
        moves = legal_moves(state, blizzards, occupied, r, c, start, goal)
        for next_state in moves:
            tentative_g_score = next_state[TIME]
            loc = next_state[LOC]
            if loc == goal:
                if tentative_g_score < best_goal_score:
                    best_goal_score = tentative_g_score
                    end_state = next_state
            h_score = heur(loc, goal)
            if tentative_g_score + h_score > best_goal_score:
                continue
            if tentative_g_score < g_score[next_state]:
                came_from[next_state] = state
                g_score[next_state] = tentative_g_score
                fn = tentative_g_score + h_score
                if not open_set_hash[next_state]:
                    heappush(open_set, (fn, next_state))
                    open_set_hash[next_state] = True

    path = [end_state]
    state = end_state
    while True:
        state = came_from.get(state, None)
        if not state:
            break
        path.append(state)
    path = list(reversed(path))
    return best_goal_score


def solve_puzzle_p2(b, o, start, goal, r, c):
    """solve maze"""

    blizzards = dict()
    occupied = dict()
    blizzards[0] = b
    occupied[0] = o

    open_set_hash = defaultdict(lambda: False)
    start_state = (0, start, 0)
    open_set_hash[start_state] = True
    open_set = [
        (float("inf"), start_state),
    ]
    came_from = dict()
    g_score = defaultdict(lambda: float("inf"))
    best_goal_score = float("inf")
    while open_set:
        _, state = heappop(open_set)
        open_set_hash[state] = False
        moves = legal_moves_2(state, blizzards, occupied, r, c, start, goal)
        for next_state in moves:
            tentative_g_score = next_state[TIME]
            loc = next_state[LOC]
            stage = next_state[STAGE]
            if loc == goal and stage == 2:
                if tentative_g_score < best_goal_score:
                    best_goal_score = tentative_g_score
                    end_state = next_state
            h_score = heur2(state, start, goal)
            if tentative_g_score + h_score > best_goal_score:
                continue
            if tentative_g_score < g_score[next_state]:
                came_from[next_state] = state
                g_score[next_state] = tentative_g_score
                fn = tentative_g_score + h_score
                if not open_set_hash[next_state]:
                    heappush(open_set, (fn, next_state))
                    open_set_hash[next_state] = True

    path = [end_state]
    state = end_state
    while True:
        state = came_from.get(state, None)
        if not state:
            break
        path.append(state)
    path = list(reversed(path))
    return best_goal_score


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    board = dict()
    walls = set()
    blizzards = []
    occupied = set()
    for y, row in enumerate(d[1:-1]):
        for x, char in enumerate(row[1:-1]):
            val = char_map[char]
            if val == WALL:
                board[(y, x)] = WALL
                walls.add((y, x))
            else:
                board[(y, x)] = OPEN
            if val in N4:
                blizzards.append((y, x, val))
                occupied.add((y, x))
    r, c = y + 1, x + 1

    start = (-1, 0)
    goal = (r, c - 1)

    result_1 = solve_puzzle(blizzards, occupied, start, goal, r, c)
    result_2 = solve_puzzle_p2(blizzards, occupied, start, goal, r, c)

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day24.txt")
        test_answer_1 = 18
        test_answer_2 = 54
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day24.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
