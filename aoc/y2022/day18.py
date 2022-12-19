""" Day 18 Solutions """

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
class Cube:
    x: int
    y: int
    z: int

    neighbors: list = None

    def __post_init__(self):
        self.neighbors = []


left = (-1, 0, 0)
right = (1, 0, 0)
front = (0, 1, 0)
back = (0, -1, 0)
top = (0, 0, 1)
bottom = (0, 0, -1)

MOVES = (left, right, front, back, top, bottom)


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    cubes = {}
    air_pockets = {}
    for row in d:
        coord = tuple(ints(row.split(",")))
        x, y, z = coord
        cubes[coord] = Cube(x=x, y=y, z=z)

    for loc, c in cubes.items():
        for move in MOVES:
            coord = loc[0] + move[0], loc[1] + move[1], loc[2] + move[2]
            if coord in cubes:
                c.neighbors.append(coord)
            elif coord in air_pockets:
                air_pockets[coord].neighbors.append(loc)
            else:
                x, y, z = coord
                air_pockets[coord] = Cube(x=x, y=y, z=z)
                air_pockets[coord].neighbors.append(loc)

    result_1 = sum(6 - len(c.neighbors) for c in cubes.values())

    from matplotlib import pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    x, y, z = zip(*cubes)
    ax.scatter(x, y, z, alpha=1.0)
    x, y, z = zip(*air_pockets)
    # ax.scatter(x, y, z)

    x, y, z = zip(*cubes)
    mins = min(x), min(y), min(z)
    maxs = max(x), max(y), max(z)
    internal_walls = 0
    external_walls = 0
    maybe_internal = []
    collected = []
    for loc, c in air_pockets.items():
        bump = 0
        for dim in range(3):
            coord = list(loc)
            while mins[dim] <= coord[dim] <= maxs[dim]:
                coord[dim] -= 1
                if tuple(coord) in cubes:
                    bump += 1
                    break
            coord = list(loc)
            while mins[dim] <= coord[dim] <= maxs[dim]:
                coord[dim] += 1
                if tuple(coord) in cubes:
                    bump += 1
                    break
        if bump == 6:
            maybe_internal.append(c)
            internal_walls += len(c.neighbors)
            if loc in collected:
                print("wtffff")
            else:
                collected.append(loc)

    x, y, z = zip(*[(c.x, c.y, c.z) for c in maybe_internal])
    ax.scatter(x, y, z, color="black", alpha=1.0)
    plt.show()

    result_2 = result_1 - internal_walls

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day18.txt")
        test_answer_1 = 64
        test_answer_2 = 58
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day18.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
