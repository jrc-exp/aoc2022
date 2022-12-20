""" Day 18 Solutions """

from argparse import ArgumentParser

from dataclasses import dataclass
from aoc.y2022.utils import load_data


def ints(x):
    return list(map(int, x))


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


def legal_moves(loc, cubes):
    moves = []
    for move in MOVES:
        coord = loc[0] + move[0], loc[1] + move[1], loc[2] + move[2]
        if coord not in cubes:
            moves.append(coord)
    return moves


def search_escape(start_state, mins, maxs, cubes):
    """search for an escape route - simplified"""
    open_set = [start_state]
    visited = set()
    escaped = False
    while not escaped and open_set:
        state = open_set.pop()
        moves = legal_moves(state, cubes)
        for next_state in moves:
            if next_state in visited:
                continue
            for dim in range(3):
                if not (mins[dim] < next_state[dim] < maxs[dim]):
                    escaped = True
                    break
            if escaped:
                break
            open_set.append(next_state)
            visited.add(next_state)
    return escaped


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

    # try to "escape" without hitting a wall:
    x, y, z = zip(*cubes)
    mins = min(x), min(y), min(z)
    maxs = max(x), max(y), max(z)

    stuck = []
    for loc, cube in air_pockets.items():
        escaped = search_escape(loc, mins, maxs, cubes)
        if not escaped:
            stuck.append(cube)

    # those are the trapped ones
    internal_walls = sum(len(c.neighbors) for c in stuck)
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
