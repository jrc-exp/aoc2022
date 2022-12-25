""" Day 25 Solutions """

import sys
from argparse import ArgumentParser
from collections import Counter, defaultdict
from itertools import permutations, product

import numpy as np

from aoc.y2022.utils import load_data


def ints(x):
    return list(map(int, x))


char_map = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}
rev_char_map = {v: k for (k, v) in char_map.items()}


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    nums = []
    for row in d:
        num = 0
        for idx, char in enumerate(reversed(row)):
            num += (5 ** idx) * char_map[char]
        nums.append(num)
    result_1_sum = sum(nums)

    z = result_1_sum
    digits = int(np.ceil(np.log10(z) / np.log10(5)))
    cts = []
    for idx in reversed(range(0, digits + 1)):
        x, z = np.divmod(z, 5 ** idx)
        cts.append(x)

    cts = list(reversed(cts))
    idx = 0
    while idx < len(cts):
        if cts[idx] == 0 and len(cts) - 1 == idx:
            break
        elif idx == len(cts) - 1:
            cts.append(0)
        while cts[idx] > 2:
            if cts[idx] == 3:
                cts[idx] = -2
                cts[idx + 1] += 1
            if cts[idx] == 4:
                cts[idx] = -1
                cts[idx + 1] += 1
            while cts[idx] >= 5:
                cts[idx] -= 5
                cts[idx + 1] += 1
        idx += 1

    cts = list(reversed(cts))
    result_1 = "".join(rev_char_map[k] for k in cts[1:])

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day25.txt")
        test_answer_1 = "2=-1=0"
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
    d = load_data("day25.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)
    assert answer_1 == "2-2=12=1-=-1=000=222"


if __name__ == "__main__":
    main()
