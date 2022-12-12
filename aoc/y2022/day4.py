""" Day 4 Solutions """

import sys
from argparse import ArgumentParser
from collections import Counter, defaultdict
from itertools import permutations, product

import numpy as np

from aoc.y2022.utils import load_data


def ints(x):
    return list(map(int, x))


def overlap(a, b, c, d):
    """quick collision check"""
    return not d < a and not b < c


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    ct = 0
    ct2 = 0
    for f in d:
        s1, s2 = f.split(",")
        s1 = list(map(int, s1.split("-")))
        s2 = list(map(int, s2.split("-")))
        if (s1[0] <= s2[0] and s1[1] >= s2[1]) or (s1[0] >= s2[0] and s1[1] <= s2[1]):
            ct += 1
        if overlap(*s1, *s2):
            ct2 += 1
    result_1 = ct
    result_2 = ct2
    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day4.txt")
        test_answer_1 = 2
        test_answer_2 = 4
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day4.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
