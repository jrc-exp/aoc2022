""" Day 24 Solutions """

from argparse import ArgumentParser
from collections import defaultdict
from heapq import heappush, heappop

from aoc.y2022.utils import load_data


# directions
U = (-1, 0)
D = (1, 0)
R = (0, 1)
L = (0, -1)
N4 = [U, D, L, R]
N5 = [U, D, L, R, (0, 0)]
char_map = {
    ">": R,
    "^": U,
    "v": D,
    "<": L,
    ".": 0,
    "#": 1,
}
# state indexes
TIME = 0
LOC = 1
STAGE = 2


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
    """manhattan distance"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def heur(state, start, goal):
    """heur2"""
    stage = state[STAGE]
    loc = state[LOC]
    h = 0
    if stage == 0:
        h += mdist(loc, goal)
        h += mdist(goal, start) * 2
    elif stage == 1:
        h += mdist(loc, start)
        h += mdist(goal, start)
    else:
        h = mdist(loc, goal)
    return h


def legal_moves(state, blizzards, occupied, r, c, start, goal):
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


def solve_puzzle(b, o, start, goal, r, c):
    """a-star search"""

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
    result_1, best_goal_score = float("inf"), float("inf")
    while open_set:
        _, state = heappop(open_set)
        open_set_hash[state] = False
        moves = legal_moves(state, blizzards, occupied, r, c, start, goal)
        for next_state in moves:
            tentative_g_score = next_state[TIME]
            loc = next_state[LOC]
            stage = next_state[STAGE]
            if loc == goal and stage == 1:
                if tentative_g_score < result_1:
                    result_1 = tentative_g_score
            if loc == goal and stage == 2:
                if tentative_g_score < best_goal_score:
                    best_goal_score = tentative_g_score
            h_score = heur(state, start, goal)
            if tentative_g_score + h_score > best_goal_score:
                continue
            if tentative_g_score < g_score[next_state]:
                came_from[next_state] = state
                g_score[next_state] = tentative_g_score
                fn = tentative_g_score + h_score
                if not open_set_hash[next_state]:
                    heappush(open_set, (fn, next_state))
                    open_set_hash[next_state] = True

    return result_1, best_goal_score


def solve(d):
    """actual solution with puzzle input"""
    # parse that puzz
    blizzards = []
    occupied = set()
    y, x = 0, 0
    for y, row in enumerate(d[1:-1]):
        for x, char in enumerate(row[1:-1]):
            val = char_map[char]
            if val in N4:
                blizzards.append((y, x, val))
                occupied.add((y, x))
    r, c = y + 1, x + 1

    # start is top left, but up one
    start = (-1, 0)
    # goal is bottom right, but down one
    goal = (r, c - 1)

    result_1, result_2 = solve_puzzle(blizzards, occupied, start, goal, r, c)

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
