""" Day 15 Solutions """

from argparse import ArgumentParser
from dataclasses import dataclass
import re

from aoc.y2022.utils import load_data


def ints(x):
    return list(map(int, x))


def mdist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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

    @property
    def ur(self):
        return (self.x - self.range // 2, self.y - self.range // 2)

    @property
    def edges(self):
        v = self.vertices
        return [
            (v[0], v[1]),
            (v[1], v[2]),
            (v[2], v[3]),
            (v[3], v[0]),
        ]

    @property
    def vertices(self):
        return [
            (self.x + self.range, self.y),
            (self.x, self.y - self.range),
            (self.x - self.range, self.y),
            (self.x, self.y + self.range),
        ]

    def __post_init__(self):
        self.range = mdist(self, self.beacon)

    def __getitem__(self, idx):
        if idx == 0:
            return self.x
        if idx == 1:
            return self.y


def line_intersection(line1, line2):
    """find line intersection"""
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception("lines do not intersect")

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


import math


def line_intersection(line1, line2):
    x1, x2, x3, x4 = line1[0][0], line1[1][0], line2[0][0], line2[1][0]
    y1, y2, y3, y4 = line1[0][1], line1[1][1], line2[0][1], line2[1][1]

    dx1 = x2 - x1
    dx2 = x4 - x3
    dy1 = y2 - y1
    dy2 = y4 - y3
    dx3 = x1 - x3
    dy3 = y1 - y3

    det = dx1 * dy2 - dx2 * dy1
    det1 = dx1 * dy3 - dx3 * dy1
    det2 = dx2 * dy3 - dx3 * dy2

    if det == 0.0:  # lines are parallel
        if det1 != 0.0 or det2 != 0.0:  # lines are not co-linear
            return None  # so no solution

        if dx1:
            if x1 < x3 < x2 or x1 > x3 > x2:
                return math.inf  # infinitely many solutions
        else:
            if y1 < y3 < y2 or y1 > y3 > y2:
                return math.inf  # infinitely many solutions

        if line1[0] == line2[0] or line1[1] == line2[0]:
            return line2[0]
        elif line1[0] == line2[1] or line1[1] == line2[1]:
            return line2[1]

        return None  # no intersection

    s = det1 / det
    t = det2 / det

    if 0.0 < s < 1.0 and 0.0 < t < 1.0:
        return x1 + t * dx1, y1 + t * dy1


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    # print("INPUT DATA:")
    # print(d)
    sensors = []
    beacons = []
    for row in d:
        sx, sy, bx, by = ints(re.findall("-?[0-9]+", row))

        beacon = Beacon(x=bx, y=by)
        if (beacon.x, beacon.y) not in [(b.x, b.y) for b in beacons]:
            beacons.append(beacon)
        sensors.append(Sensor(x=sx, y=sy, beacon=beacon))

    if len(d) == 14:
        target_y = 10
        max_dim = 20
    else:
        target_y = 2000000
        max_dim = 4000000

    minx = min(s.x - s.range for s in sensors)
    maxx = max(s.x + s.range for s in sensors)
    ct = 0

    sub_sensors = list(filter(lambda s: s.range - s.y <= target_y <= s.range + s.y, sensors))
    x = minx
    while x < maxx:
        pt = (x, target_y)
        jump = False
        s = sub_sensors[0]
        for s in sub_sensors:
            if mdist(s, pt) <= s.range:
                jump = True
                break
        if jump:
            jump_size = max(s.range - mdist(s, pt), 1)
            ct += jump_size
            x += jump_size
        else:
            x += 1

    ct -= sum(minx <= b.x <= maxx for b in beacons if b.y == target_y)
    result_1 = ct

    """
    goal_line = ((-1e9, target_y), (1e9, target_y))
    x_pairs = []
    for s in sensors:
        intersections = []
        for edge in s.edges:
            isect = line_intersection(edge, goal_line)
            if isinstance(isect, tuple):
                intersections.append(isect)
        xs = sorted(x[0] for x in intersections)
        if xs:
            x_pairs.append(xs)

    def overlap(a, b, c, d):
        "quick collision check"
        return not d < a and not b < c

    x_pairs = sorted(x_pairs)
    merging = True
    print(x_pairs)
    while merging:
        for idx in range(len(x_pairs) - 1):
            if overlap(*x_pairs[idx], *x_pairs[idx + 1]):
                x_pairs[idx] = x_pairs[idx][0], x_pairs[idx + 1][1]
                del x_pairs[idx + 1]
                break
        else:
            merging = False
    b_ct = 0
    for beacon in beacons:
        if beacon.y == target_y:
            for x_pair in x_pairs:
                if overlap(*x_pair, beacon.x, beacon.x):
                    b_ct += 1

    result_1 = sum(x[1] - x[0] + 1 for x in x_pairs) - b_ct
    """

    from time import time

    winner = None
    start = time()
    for sensor in sensors:
        check_pts = []
        for edge in sensor.edges:
            for s in sensors:
                if s == sensor:
                    continue
                for edge2 in s.edges:
                    pt = line_intersection(edge, edge2)
                    if isinstance(pt, tuple):
                        check_pts.append(pt)
        for vertex in sensor.vertices + check_pts:
            moves = ((0, 1), (0, -1), (-1, 0), (1, 0))
            for move in moves:
                loc = vertex[0] + move[0], vertex[1] + move[1]
                if (0 <= loc[0] <= max_dim) and (0 <= loc[1] <= max_dim):
                    no_one = True
                    for s in sensors:
                        if mdist(s, loc) <= s.range:
                            no_one = False
                    if no_one:
                        winner = loc
                        result_2 = winner[0] * 4000000 + winner[1]
                        print("Part two took...", time() - start)
                        return result_1, result_2

    result_2 = winner[0] * 4000000 + winner[1]

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
        test_answer_2 = 56000011
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

"""
    plot = False
    if plot:
        from matplotlib import pyplot as plt
        from matplotlib.patches import Polygon

        plt.figure()
        ax = plt.subplot(111)
        for s in sensors:
            x1, y1 = s.x, s.y - s.range
            x2, y2 = s.x - s.range, s.y
            x3, y3 = s.x, s.y + s.range
            x4, y4 = s.x + s.range, s.y

            xy = [
                (x1, y1),
                (x2, y2),
                (x3, y3),
                (x4, y4),
            ]

            ax.add_patch(Polygon(xy, closed=True, alpha=0.25, edgecolor="black"))

            x1, y1 = s.x, s.y - 1
            x2, y2 = s.x - 1, s.y
            x3, y3 = s.x, s.y + 1
            x4, y4 = s.x + 1, s.y

            xy = [
                (x1, y1),
                (x2, y2),
                (x3, y3),
                (x4, y4),
            ]

            ax.add_patch(Polygon(xy, closed=True, alpha=0.25, color="black"))

        for s in beacons:
            x1, y1 = s.x, s.y - 1
            x2, y2 = s.x - 1, s.y
            x3, y3 = s.x, s.y + 1
            x4, y4 = s.x + 1, s.y

            xy = [
                (x1, y1),
                (x2, y2),
                (x3, y3),
                (x4, y4),
            ]

            ax.add_patch(Polygon(xy, closed=True, alpha=0.25, color="red"))

        plt.xlim([0, max_dim + 0])
        plt.ylim([max_dim + 0, 0])
        plt.show()
        result_2 = int(input("X Value:")) * 4000000 + int(input("Y Value:"))
"""
