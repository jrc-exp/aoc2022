""" Day 5 Solutions """

import sys
from argparse import ArgumentParser
from collections import Counter, defaultdict
from itertools import permutations, product

import numpy as np

from aoc.y2022.utils import load_data


def ints(x):
    return list(map(int, x))


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)

    for idx, row in enumerate(d):
        if row[1] == "1":
            n_col = int(row[-1])
            key_row = idx
            break
    cols = [list() for _ in range(n_col)]
    print("Number of cols: ", n_col)
    for row in reversed(d[:key_row]):
        print(row)
        for col in range(n_col):
            if len(row) > 1 + 4 * col and row[1 + 4 * col] != " ":
                cols[col].append(row[1 + 4 * col])
    print(cols)

    from copy import deepcopy

    cols2 = deepcopy(cols)

    for row in d[key_row + 2 :]:
        row = row.split(" ")
        ct, fr, to = list(map(int, [row[1], row[3], row[5]]))
        cols2[to - 1].extend(cols2[fr - 1][-ct:])
        for _ in range(ct):
            cols[to - 1].append(cols[fr - 1].pop())
            cols2[fr - 1].pop()

    result_1 = "".join([c[-1] for c in cols])

    print(cols2)

    result_2 = "".join([c[-1] for c in cols2])

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day5.txt")
        test_answer_1 = "CMZ"
        test_answer_2 = "MCD"
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day5.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
