""" Day 8 Solutions """

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

    n = len(d[0])
    visible = set()
    grid = np.array([ints(r) for r in d])
    best = 0
    for j in range(n):
        for k in range(n):
            if j == 0 or k == 0 or j == n - 1 or k == n - 1:
                visible.add((j, k))
                continue
            h = grid[j, k]
            row = grid[j, :]
            col = grid[:, k]
            if max(row[:k]) < h or max(row[k + 1 :]) < h:
                visible.add((j, k))
            if max(col[:j]) < h or max(col[j + 1 :]) < h:
                visible.add((j, k))
            scores = []
            # up
            loc = j
            score = 0
            while loc > 0:
                loc -= 1
                score += 1
                if grid[loc, k] >= h:
                    break
            scores.append(score)
            # left
            loc = k
            score = 0
            while loc > 0:
                loc -= 1
                score += 1
                if grid[j, loc] >= h:
                    break
            scores.append(score)
            # down
            loc = j
            score = 0
            while loc < n - 1:
                print(loc)
                loc += 1
                score += 1
                if grid[loc, k] >= h:
                    break
            scores.append(score)
            # right
            loc = k
            score = 0
            while loc < n - 1:
                loc += 1
                score += 1
                if grid[j, loc] >= h:
                    break
            scores.append(score)
            score = scores[0] * scores[1] * scores[2] * scores[3]
            print((j, k), scores, score)
            if score > best:
                best = score

    result_1 = len(visible)
    result_2 = best
    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day8.txt")
        test_answer_1 = 21
        test_answer_2 = 8
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day8.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
