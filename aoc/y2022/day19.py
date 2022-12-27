""" Day 19 Solutions """

import re
from argparse import ArgumentParser
from heapq import heappush, heappop
from math import ceil, prod
from multiprocessing import Pool

from aoc.y2022.utils import load_data


def strip_ints(x):
    return ints(re.findall("-?[0-9]+", x))


def ints(x):
    return list(map(int, x))


# state indices
ind = {
    "ore": 0,
    "clay": 1,
    "obsidian": 2,
    "geode": 3,
}
MOVE = 8


def mine(state, steps=1):
    if steps > 1:
        state = mine(state, steps - 1)
    move = state[MOVE]
    return (
        state[0],
        state[1],
        state[2],
        state[3],
        state[0] + state[4],
        state[1] + state[5],
        state[2] + state[6],
        state[3] + state[7],
        move + 1,
    )


def build(state, bot, cost):
    """Build a robot"""
    new_state = list(state)
    new_state[ind[bot]] += 1
    for material, price in cost[bot].items():
        new_state[ind[material] + 4] -= price
    return tuple(new_state)


def could_build(state, cost, max_moves):
    """bots that could be built and when from this state"""
    build_list = []
    move = state[MOVE]
    for bot, prices in cost.items():
        highest_build_step = 0
        for material, price in prices.items():
            bots = state[ind[material]]
            if bots == 0:
                break
            stock = state[ind[material] + 4]
            steps = ceil((price - stock) / bots)
            if steps > highest_build_step:
                highest_build_step = steps
        else:
            if move + highest_build_step < max_moves - 1:
                s = mine(state, steps=highest_build_step) if highest_build_step else state
                build_list.append((bot, s))
    next_states = [build(mine(s), b, cost) for (b, s) in build_list]
    return next_states


def legal_moves_bots(state, max_moves, cost):
    """legal moves bots only"""
    move = state[MOVE]
    move_rem = max_moves - move
    if move_rem <= 0:
        return []
    return could_build(state, cost, max_moves)


def heur(state, max_moves=24):
    """
    Simple heuristic is - build a new geode bot at every next step
    """
    move = state[MOVE]
    moves = max_moves - move
    return ((moves) * (moves - 1)) / 2


def solve_puzzle(cost, max_moves=24):
    """solve maze"""

    start_state = (1, 0, 0, 0, 0, 0, 0, 0, 0)

    open_set = [
        (0, start_state),
    ]
    best_goal_score = 0

    visited = set()
    while open_set:
        fn, state = heappop(open_set)
        if state[MOVE] == max_moves:
            continue
        for next_state in legal_moves_bots(state, cost=cost, max_moves=max_moves):
            if next_state in visited:
                continue
            # update state score and heuristic:
            move_rem = max_moves - next_state[MOVE]
            tentative_g_score = next_state[ind["geode"] + 4] + next_state[ind["geode"]] * move_rem
            h_score = heur(next_state, max_moves)

            # bail if this can't possible improve
            if tentative_g_score + h_score < best_goal_score:
                continue

            if tentative_g_score > best_goal_score:
                best_goal_score = tentative_g_score

            fn = tentative_g_score + h_score
            heappush(open_set, (-fn, next_state))
            visited.add(next_state)

    return best_goal_score


def sp2(x):
    """needed to call in p.map for multiprocessing..."""
    return solve_puzzle(x, max_moves=32)


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
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

    # part 1 - all blueprints for 24 steps
    with Pool(len(costs)) as p:
        values = p.map(solve_puzzle, costs)
        result_1 = sum(v * (idx + 1) for idx, v in enumerate(values))

    # part 2 - first three blueprints for 30 steps
    max_nodes = 3
    with Pool(max_nodes) as p:
        scores = p.map(sp2, costs[:max_nodes])

    result_2 = prod(scores)
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
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day19.txt")
    answer_1, answer_2 = solve(d)
    # answer_2 = 28 * 38 * 44
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
