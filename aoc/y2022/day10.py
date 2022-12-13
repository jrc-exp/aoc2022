""" Day 10 Solutions """

import sys
from argparse import ArgumentParser
from collections import Counter, defaultdict
from itertools import permutations, product
from dataclasses import dataclass

import numpy as np

from aoc.y2022.utils import load_data


def ints(x):
    return list(map(int, x))


@dataclass
class Computer:
    """Computer class"""

    _cycle = 0
    x = 1
    signal_strength = 0
    crt = None

    def __post_init__(self):
        self.crt = [list("." * 40) for _ in range(6)]

    @property
    def cycle(self):
        return self._cycle

    @cycle.setter
    def cycle(self, val):
        row = self.cycle // 40
        col = self.cycle % 40
        if col - 1 <= self.x <= col + 1:
            self.crt[row][col] = "#"

        self._cycle = val
        if (self.cycle - 20) % 40 == 0:
            self.signal_strength += self.cycle * self.x

    def execute(self, cmd):
        self.cycle += 1
        if cmd.startswith("noop"):
            pass
        if cmd.startswith("addx"):
            self.cycle += 1
            self.x += int(cmd.split(" ")[1])


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    pc = Computer()
    for row in d:
        pc.execute(row)
    result_1 = pc.signal_strength

    for row in pc.crt:
        print("".join(row))

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day10.txt")
        test_answer_1 = 13140
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
    d = load_data("day10.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
