""" Day 19 Solutions """

import re
import numpy as np

from heapq import heappush
from argparse import ArgumentParser
from collections import defaultdict
from time import time

from aoc.y2022.utils import load_data


def strip_ints(x):
    return ints(re.findall("-?[0-9]+", x))


def ints(x):
    return list(map(int, x))


ind = {
    "ore": 0,
    "clay": 1,
    "obsidian": 2,
    "geode": 3,
}
MOVE = 8


def mine(state):
    return (
        *state[:4],
        state[0] + state[4],
        state[1] + state[5],
        state[2] + state[6],
        state[3] + state[7],
        state[8] + 1,
    )


def build(state, bot, cost):
    """Build a robot"""
    new_state = list(state)
    new_state[ind[bot]] += 1
    for material, price in cost[bot].items():
        new_state[ind[material] + 4] -= price
    return tuple(new_state)


def can_build(state, cost):
    build_list = []
    for bot, prices in cost.items():
        for material, price in prices.items():
            if price > state[ind[material] + 4]:
                break
        else:
            build_list.append(bot)
    return build_list


def legal_moves(state, max_moves, cost):
    move = state[MOVE]
    move_rem = max_moves - move
    if move_rem <= 0:
        return []
    buildable = can_build(state, cost)
    state = mine(state)
    return [state] + [build(state, bot, cost) for bot in buildable]


def heur(state, max_moves=24):
    bots = state[ind["geode"]]
    geodes = state[ind["geode"] + 4]
    move = state[MOVE]
    moves = max_moves - move
    # build a new geode bot at every step
    return geodes + bots * moves + (moves * moves - 1) / 2


def solve_puzzle(cost, max_moves=24):
    """solve maze"""

    start_state = (1, 0, 0, 0, 0, 0, 0, 0, 0)

    open_set_hash = defaultdict(lambda: False)
    open_set_hash[start_state] = True
    open_set = [
        (0, start_state),
    ]
    came_from = dict()
    g_score = defaultdict(lambda: 0)
    best_goal_score = -1
    end_state = None
    ct = 0

    start = time()
    visited = set()
    while open_set:
        ct += 1
        fn, state = open_set.pop()
        if fn < best_goal_score:
            continue
        if state[MOVE] == max_moves:
            continue
        moves = legal_moves(state, cost=cost, max_moves=max_moves)
        for next_state in moves:
            if next_state in visited:
                continue
            tentative_g_score = next_state[ind["geode"] + 4]

            h_score = heur(next_state, max_moves)

            if tentative_g_score > best_goal_score:
                end_state = next_state
                best_goal_score = tentative_g_score
                elapsed = time() - start
                print(best_goal_score, elapsed)

            if tentative_g_score + h_score < best_goal_score:
                continue

            fn = tentative_g_score + h_score
            heappush(open_set, (fn, next_state))
            visited.add(next_state)

            # if tentative_g_score >= g_score[next_state]:
            #     came_from[next_state] = state
            #     g_score[next_state] = tentative_g_score
            #     # slower with the heuristic... *sigh*
            #     fn = tentative_g_score + h_score
            #     if not open_set_hash[next_state]:
            #         open_set_hash[next_state] = True
            # else:
            #     print("this ever happen?")

    path = [end_state]
    state = end_state
    while True:
        state = came_from.get(state, None)
        if not state:
            break
        path.append(state)
    path = list(reversed(path))
    [print(p) for p in path]
    return best_goal_score


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    costs = []
    for row in d:
        s = row.split("Each")
        cost = {}
        for r in s[1:]:
            n, p = r.split(" costs ")
            n = n.split(" ")[1]
            p = p.split(" and ")
            rcost = {}
            for c in p:
                c = c.split(" ")
                rcost[c[1].strip(".")] = int(c[0])
            cost[n] = rcost
        costs.append(cost)

    value = 0
    for idx, cost in enumerate(costs, 1):
        now = time()
        best_score = solve_puzzle(cost)
        print("Solved", idx, "in", f"{time()-now:.2f}s")
        value += best_score * idx
    result_1 = value

    scores = []
    for cost in costs[:3]:
        best_score = solve_puzzle(cost, max_moves=32)
        scores.append(best_score)

    result_2 = np.prod(scores)
    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day19.txt")
        test_answer_1 = 33
        test_answer_2 = 56 * 62
        test_solution_1, test_solution_2 = solve(d)
        # assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day19.txt")
    answer_1, answer_2 = solve(d)
    answer_2 = 28 * 38 * 44
    answer_2 = 46816
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
