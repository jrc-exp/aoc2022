""" Day 15 Solutions """

import sys
from argparse import ArgumentParser
from collections import Counter, defaultdict
from itertools import permutations, product
import re

import numpy as np

from aoc.y2022.utils import load_data


def ints(x):
    return list(map(int, x))


def mdist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


from dataclasses import dataclass


@dataclass
class Beacon:
    x: int
    y: int

    def __getitem__(self, idx):
        if idx == 0:
            return self.x
        if idx == 1:
            return self.y


@dataclass
class Sensor:
    """Sensor!"""

    x: int
    y: int
    beacon: Beacon
    range = 0

    def __post_init__(self):
        self.range = mdist(self, self.beacon)

    def __getitem__(self, idx):
        if idx == 0:
            return self.x
        if idx == 1:
            return self.y


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    sensors = []
    beacons = []
    for row in d:
        sx, sy, bx, by = ints(re.findall("[0-9]+", row))

        beacons.append(Beacon(x=bx, y=by))
        sensors.append(Sensor(x=sx, y=sy, beacon=beacons[-1]))

    if len(d) == 14:
        target_y = 10
    else:
        target_y = 2000000

    miny = min(s.y - s.range for s in sensors)
    maxy = max(s.y + s.range for s in sensors)
    minx = min(s.x - s.range for s in sensors)
    maxx = max(s.x + s.range for s in sensors)
    ct = 0
    from tqdm.auto import tqdm

    sensors = list(filter(lambda s: s.range - s.y <= target_y <= s.range + s.y, sensors))
    for x in tqdm(range(minx, maxx + 1)):
        pt = (x, target_y)
        isnt = False
        if any(pt == (b.x, b.y) for b in beacons + sensors):
            continue
        for s in sensors:
            if mdist(s, pt) <= s.range:
                isnt = True
                break
        if isnt:
            ct += 1

    result_1 = ct

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day15.txt")
        test_answer_1 = 26
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
    d = load_data("day15.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
