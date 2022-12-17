""" Day 16 Solutions """

import sys
from argparse import ArgumentParser
from collections import Counter, defaultdict
from itertools import permutations, product

import numpy as np

from aoc.y2022.utils import load_data


def ints(x):
    return list(map(int, x))


def de2bi(x, l=10):
    return ints(format(x, f"#0{l+2:d}b")[2:])


from heapq import heappush

FLOW = 0
MOVE = 1
VALVE = 2
LOC = 3


def bit_set(x, bit):
    return (x & (1 << bit)) >> bit


def set_bit(x, bit):
    return x | (1 << bit)


def legal_moves(state, dests):
    """Return legal moves"""
    valve = state[VALVE]
    return [idx for idx in dests if not bit_set(valve, idx)]


def flow(valves, rates):
    rate = 0
    for idx in rates:
        rate += bit_set(valves, idx) * rates[idx]
    return rate


def heur(state, rates, dists, max_moves=30):
    """Calculate heuristic"""
    loc = state[LOC]
    move_number = state[MOVE]
    if move_number >= max_moves - 1:
        return 0
    max_moves_remaining = max_moves - move_number
    valves = state[VALVE]
    h = flow(valves, rates) * max_moves_remaining

    for idx in rates:
        if rates[idx] and not bit_set(valves, idx):
            h += rates[idx] * max(0, max_moves_remaining - dists[(loc, idx)])

    return h


def find_goal(start, goal, path, neighbors):
    """Find a path from a node to another node"""
    if goal in neighbors[start]:
        return path + [start, goal]
    for node in neighbors[start]:
        visited = set(a for a in path)
        if node not in visited:
            goal_path = find_goal(node, goal, path + [start], neighbors)
            if goal_path is not None:
                return goal_path
    return None


from aoc.y2022.utils import dijkstra_algorithm


def solve_puzzle(edges, rates, alpha_valves, max_moves=30):
    """solve maze"""

    # list of distances from node to node
    dists = dict()
    # valid destinations that can turn on flow
    dests = [node for node in rates if rates[node]]
    print(dests)
    for edge in [
        0,
    ] + dests:
        _, short_path = dijkstra_algorithm(edges, edge)
        for edge2 in dests:
            if edge != edge2:
                dists[(edge, edge2)] = short_path[edge2]

    print(dists)

    max_flow = sum(flow for flow in rates.values())

    open_set_hash = defaultdict(lambda: False)
    # state = (move number, valve state, cumulative flow, location)
    start_state = (0, 0, 0, 0)
    open_set_hash[start_state] = True
    open_set = [
        (0, start_state),
    ]
    came_from = dict()
    g_score = defaultdict(lambda: 0)
    best_goal_score = -1
    goal_valve = 0
    for idx in rates:
        if rates[idx]:
            goal_valve = set_bit(goal_valve, idx)

    end_state = None
    ct = 0
    while open_set:
        ct += 1
        _, state = open_set.pop()
        open_set_hash[state] = False
        curr_loc = state[LOC]
        if state[MOVE] == max_moves:
            continue
        moves = legal_moves(state, dests)
        if not moves:
            moves = [None]
        for next_loc in moves:
            if next_loc is None:
                # if we're out of legal moves - just sit here
                n_steps = max_moves - state[MOVE]
                next_loc = curr_loc
            else:
                # if we have a legal move
                n_steps = dists[(curr_loc, next_loc)] + 1
                # can't do it if it takes too long
                if state[MOVE] + n_steps >= max_moves:
                    # we're off the end so let's tally the score
                    n_steps = max_moves - state[MOVE]
                    move_number = max_moves
            move_number = state[MOVE] + n_steps
            valve = state[VALVE]
            state_flow_rate = flow(valve, rates)
            valve = set_bit(valve, next_loc)
            tentative_g_score = state[FLOW] + state_flow_rate * n_steps
            next_state = (tentative_g_score, move_number, valve, next_loc)

            h_score = 0  # float("inf")  # heur(next_state, max_moves=max_moves, rates=rates, dists=dists)

            # stop condition - out of moves!
            if max_moves == move_number:
                full_score = tentative_g_score
                if full_score > best_goal_score:
                    print("best score!", full_score, next_state, state)
                    end_state = next_state
                    best_goal_score = full_score
                    g_score[next_state] = full_score
                    came_from[next_state] = state
                    continue
                continue

            if tentative_g_score >= g_score[next_state]:
                came_from[next_state] = state
                g_score[next_state] = tentative_g_score
                if tentative_g_score > best_goal_score:
                    best_goal_score = tentative_g_score
                # slower with the heuristic... *sigh*
                fn = g_score[next_state] + h_score
                if not open_set_hash[next_state]:
                    heappush(open_set, (fn, next_state))
                    open_set_hash[next_state] = True

    print(ct, "steps")

    path = [end_state]
    state = end_state
    while True:
        state = came_from.get(state, None)
        if not state:
            break
        path.append(state)
    path = list(reversed(path))

    print(path)
    print_path = True
    valve = 0
    if print_path:
        last_loc = 0
        output = 0
        f = 0
        idx = 0
        for p in path[1:]:
            n_steps = dists.get((last_loc, p[LOC]), 100)
            idx += n_steps
            # MOVE
            output += f * n_steps
            if idx > 30:
                continue
            print("== Minute %d ==" % idx)
            print("Releasing %d pressure. (Total=%d)" % (f, output))

            letter = alpha_valves[p[LOC]]
            print("You move to valve", letter)

            # OPEN
            output += f
            idx += 1
            print("== Minute %d ==" % idx)
            print("Releasing %d pressure. (Total=%d)" % (f, output))
            print("You open", letter)
            print()
            if idx < 30:
                valve = set_bit(valve, p[LOC])
                f = flow(valve, rates)

            last_loc = p[LOC]
        print("Total=", output + f * (30 - idx))

    return best_goal_score


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)

    alpha_valves = []
    alpha_edges = dict()
    alpha_rates = dict()
    for row in d:
        valve = row[6:].split(" ")[0]
        rate = int(row[row.index("rate=") + 5 :].split(";")[0])
        if "valves " in row:
            tunnels = row[row.index("valves ") + 7 :].split(", ")
        else:
            tunnels = row[row.index("valve ") + 6 :].split(", ")
        alpha_valves.append(valve)
        alpha_rates[valve] = rate
        alpha_edges[valve] = tunnels

    # remap to ints
    valves = list(range(len(alpha_valves)))
    edges = {idx: alpha_edges[alpha_valves[idx]] for idx in valves}
    for key in edges:
        edges[key] = [alpha_valves.index(edge) for edge in edges[key]]
    rates = {idx: alpha_rates[alpha_valves[idx]] for idx in valves}

    result_1 = solve_puzzle(edges, rates, alpha_valves=alpha_valves)

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day16.txt")
        test_answer_1 = 1651
        test_answer_2 = 0
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day16.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
