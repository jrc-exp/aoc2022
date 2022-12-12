""" Day 9 Solutions """

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
class RopeHead:
    """Rope Head"""

    x: int = 0
    y: int = 0

    @property
    def loc(self):
        return (self.y, self.x)

    def move(self, direction):
        if direction == "L":
            self.x -= 1
        if direction == "R":
            self.x += 1
        if direction == "U":
            self.y += 1
        if direction == "D":
            self.y -= 1


@dataclass
class RopeTail(RopeHead):
    """Rope Tail"""

    visited = set()

    def follow(self, head):
        """Follow"""
        mlr = False
        mud = False
        if head.y - self.y > 1:
            self.move("U")
            mud = True
        if head.y - self.y < -1:
            self.move("D")
            mud = True
        if head.x - self.x > 1:
            self.move("R")
            mlr = True
        if head.x - self.x < -1:
            self.move("L")
            mlr = True

        if mlr:
            if head.y - self.y == 1:
                self.move("U")
            elif head.y - self.y == -1:
                self.move("D")

        if mud:
            if head.x - self.x == 1:
                self.move("R")
            elif head.x - self.x == -1:
                self.move("L")

        self.visited.add(self.loc)


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    # print(d)
    head = RopeHead()
    tail = RopeTail()

    for row in d:
        direction, ct = row.split(" ")
        ct = int(ct)
        for _ in range(ct):
            head.move(direction)
            tail.follow(head)
    result_1 = len(tail.visited)

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day9.txt")
        test_answer_1 = 13
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
    d = load_data("day9.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
