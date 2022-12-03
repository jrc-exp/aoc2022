""" Day 3 Solutions """

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

    from string import ascii_lowercase, ascii_uppercase

    priority = {a: idx + 1 for (idx, a) in enumerate(ascii_lowercase + ascii_uppercase)}

    vals = []
    for row in d:
        a, b = row[: len(row) // 2], row[len(row) // 2 :]
        for letter in a:
            if letter in b:
                vals.append(priority[letter])
                break

    result_1 = sum(vals)

    vals = []
    for idx in range(0, len(d), 3):
        for letter in d[idx]:
            if letter in d[idx + 1] and letter in d[idx + 2]:
                vals.append(priority[letter])
                break

    result_2 = sum(vals)

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day3.txt")
        test_answer_1 = 157
        test_answer_2 = 70
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day3.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
