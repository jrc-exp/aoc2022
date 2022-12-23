""" Day 23 Solutions """

import sys
from argparse import ArgumentParser
from collections import Counter, defaultdict
from itertools import permutations, product

import numpy as np

from aoc.y2022.utils import load_data


def ints(x):
    return list(map(int, x))


NBR8 = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 0),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]
I = (0, 0)
N = (-1, 0)
NE = (-1, 1)
NW = (-1, -1)
S = (1, 0)
SE = (1, 1)
SW = (1, -1)
E = (0, 1)
W = (0, -1)
NBR8 = [N, NE, NW, S, SE, SW, E, W]


def print_board(board):
    """
    Print the board
    """
    print("board", list(sorted(board)))
    ymin = min(-2, min(y for (y, x) in board))
    xmin = min(-3, min(x for (y, x) in board))
    ymax = max(9, max(y for (y, x) in board))
    xmax = max(10, max(x for (y, x) in board))

    for y in range(ymin, ymax + 1):
        row = ""
        for x in range(xmin, xmax + 1):
            if (y, x) in board:
                row += "#"
            else:
                row += "."
        print(row)


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0

    board = defaultdict(lambda: False)
    elves = set()
    for y, row in enumerate(d):
        for x, char in enumerate(row):
            if char == "#":
                board[y, x] = True
                elves.add((y, x))

    proposed_moves = []
    groups = [
        NBR8,
        [N, NE, NW],
        [S, SE, SW],
        [W, NW, SW],
        [E, NE, SE],
    ]
    dests = [None, N, S, W, E]

    print("Starting Board")
    print_board(elves)

    n = len(elves)
    moved = True
    ct = 0
    while moved:
        ct += 1
        proposed_moves = []
        proposals = defaultdict(lambda: 0)
        for elf in elves:
            for idx, group in enumerate(groups):
                if not any(((move[0] + elf[0], move[1] + elf[1]) in elves) for move in group):
                    move = dests[idx]
                    if move is None:
                        dest = None
                    else:
                        dest = move[0] + elf[0], move[1] + elf[1]
                    proposed_moves.append((elf, dest))
                    proposals[dest] += 1
                    break
            else:
                proposed_moves.append((elf, None))
        # todo - rotate dests
        dests = dests[:1] + dests[2:] + dests[1:2]
        groups = groups[:1] + groups[2:] + groups[1:2]
        moved = False
        elves = set()
        for idx in range(n):
            elf, dest = proposed_moves[idx]
            if dest is not None and proposals[dest] == 1:
                elves.add(dest)
                moved = True
            else:
                elves.add(elf)
        if ct == 10:
            ymin = min(y for (y, _) in elves)
            xmin = min(x for (_, x) in elves)
            ymax = max(y for (y, _) in elves)
            xmax = max(x for (_, x) in elves)

            result_1 = (xmax - xmin + 1) * (ymax - ymin + 1) - n

    result_2 = ct

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day23.txt")
        test_answer_1 = 110
        test_answer_2 = 20
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day23.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
