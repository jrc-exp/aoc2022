""" Day 17 Solutions """

from copy import deepcopy
from itertools import cycle
from argparse import ArgumentParser

import numpy as np

from aoc.y2022.utils import load_data


def ints(x):
    return list(map(int, x))


flat_line = ((0, 0), (1, 0), (2, 0), (3, 0))
plus = (
    (1, 2),
    (1, 0),
    (0, 1),
    (1, 1),
    (2, 1),
)
l_shape = ((2, 2), (2, 0), (2, 1), (1, 0), (0, 0))
vert_line = (
    (0, 3),
    (0, 0),
    (0, 1),
    (0, 2),
)
square = ((0, 1), (0, 0), (1, 0), (1, 1))
shapes = (flat_line, plus, l_shape, vert_line, square)

MOVE = {
    "<": -1,
    ">": 1,
}


def blow(rock, move, board):
    new_rock = deepcopy(rock)
    for pt in new_rock:
        pt[0] += move
        if pt[0] >= 7 or pt[0] < 0:
            return rock
    if any(tuple(pt) in board for pt in new_rock):
        return rock
    return new_rock


def fall(rock, board):
    new_rock = deepcopy(rock)
    for pt in new_rock:
        pt[1] -= 1
    if any(tuple(pt) in board for pt in new_rock):
        return rock, False
    return new_rock, True


def make_rock(max_y, shape_cycle):
    rock = [list(l) for l in next(shape_cycle)]
    start_y = max_y + 3
    start_x = 2
    for pt in rock:
        pt[0] += start_x
        pt[1] += start_y
    return rock


def print_board(board, max_y):
    for y in reversed(range(-1, max_y + 3)):
        line = ["#" if (x, y) in board else "." for x in range(7)]
        line = "".join(line)
        print(line)


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0

    shape_cycle = cycle(shapes)

    moves = map(lambda x: MOVE[x], d[0])
    moves = cycle(moves)
    max_y = 0
    board = set((x, -1) for x in range(7))
    moving = False
    ct = 0
    cts = [
        0,
    ]
    step_size = 1000
    while ct < 8001:
        move = next(moves)
        if not moving:
            rock = make_rock(max_y, shape_cycle)
            moving = True
        rock = blow(rock, move, board)
        rock, moving = fall(rock, board)
        if not moving:
            for pt in rock:
                board.add(tuple(pt))
            max_y = max(max_y, rock[0][1] + 1)
            ct += 1
            if ct == 2022:
                result_1 = max_y
            if ct % step_size == 0:
                cts.append(max_y)

    # How did I come up with this crap?
    loop = list(map(int, np.diff(cts)))
    target = 1000000000000
    total = target - step_size
    result_2 = (total // (7 * step_size)) * sum(loop[1:8]) + loop[0] + sum(loop[1 : (total % (7 * step_size)) // step_size + 1])

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day17.txt")
        test_answer_1 = 3068
        test_answer_2 = 1514285714288
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day17.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
