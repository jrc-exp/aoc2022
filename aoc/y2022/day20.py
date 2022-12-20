""" Day 20 Solutions """

import sys
from argparse import ArgumentParser
from collections import Counter, defaultdict
from itertools import permutations, product

import numpy as np

from aoc.y2022.utils import load_data


def ints(x):
    return list(map(int, x))


from dataclasses import dataclass


@dataclass
class Point:
    """POINT"""

    x: int
    N: int
    head = None
    tail = None
    primary = False

    def swap(self, pt, d):
        """swap two pts"""
        if self.primary:
            self.primary = False
            self.head.primary = True
        if d == "left":
            left, right = pt, self
        else:
            left, right = self, pt
        left.head = right.head
        right.tail = left.tail

        right.head = left
        left.tail = right

        right.tail.head = right
        left.head.tail = left

    def move_left(self):
        self.swap(self.tail, "left")

    def move_right(self):
        self.swap(self.head, "right")


def get_list(pts):
    pt = pts[0]
    for pt in pts:
        if pt.primary:
            break
    out = []
    for _ in range(len(pts)):
        out.append(pt.x)
        pt = pt.head
    return out


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    n = ints(d)
    pts = []
    for idx, x in enumerate(n):
        pts.append(Point(x=x, N=len(n)))

    N = len(pts)
    for idx, pt in enumerate(pts):
        if idx == 0:
            pt.primary = True
        pt.head = pts[(idx + 1) % N]
        pt.tail = pts[idx - 1]

    for idx, pt in enumerate(pts):
        for _ in range(abs(pt.x)):
            if pt.x < 0:
                pt.move_left()
            else:
                pt.move_right()

    vals = get_list(pts)

    zero = vals.index(0)
    result_1 = 0
    for offset in (1000, 2000, 3000):
        result_1 += vals[(zero + offset) % N]

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day20.txt")
        test_answer_1 = 3
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
    d = load_data("day20.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
