""" Day 12 Solutions """

from argparse import ArgumentParser
from heapq import heappush, heappop
from functools import cache

from aoc.y2022.utils import load_data


def solve(d):
    """actual solution with puzzle input"""

    heights = [list(row) for row in d]
    nodes = []
    sources = []
    for j, row in enumerate(heights):
        for k, val in enumerate(row):
            nodes.append((j, k))
            if val == "E":
                exit_node = (j, k)
                heights[j][k] = 26
            elif val == "S":
                start_node = (j, k)
                heights[j][k] = 1
            else:
                heights[j][k] = ord(val) - ord("a") + 1

            if heights[j][k] == 1:
                sources.append((j, k))

    @cache
    def neighbors(loc):
        U = (+1, 0)
        D = (-1, 0)
        L = (0, -1)
        R = (0, 1)
        legal_moves = U, D, L, R
        neighbors = []
        h = heights[loc[0]][loc[1]]
        for move in legal_moves:
            dest = (loc[0] + move[0], loc[1] + move[1])
            if in_bounds(dest):
                h2 = heights[dest[0]][dest[1]]
                if h - h2 >= -1:
                    neighbors.append(dest)
        return neighbors

    @cache
    def in_bounds(coord):
        if coord[0] < 0 or coord[0] >= len(heights):
            return False
        if coord[1] < 0 or coord[1] >= len(heights[0]):
            return False
        return True

    def search(nodes, source):
        """searching"""
        dist = dict()
        prev = dict()
        in_q = dict()
        q = []
        dist[source] = 0
        for v in nodes:
            if v != source:
                dist[v] = float("inf")
                prev[v] = None
            in_q[v] = True
            heappush(q, (dist[v], v))

        while q:
            _, u = heappop(q)
            in_q[u] = False
            for v in neighbors(u):
                d = dist[u] + 1
                if d < dist[v]:
                    prev[v] = u
                    if not in_q[v]:
                        # ideally you'd want to update the entry
                        # for this value if it's already here,
                        # but it's too slow in python!
                        heappush(q, (d, v))
                    dist[v] = d
                    if v == exit_node:
                        return dist, prev
        return dist, prev

    dist, prev = search(nodes, start_node)
    node = exit_node
    path = []
    while node != start_node:
        path.append(node)
        node = prev[node]
    path.append(node)

    result_1 = dist[exit_node]

    best = float("inf")
    ct = 0
    for source in sources:
        ct += 1
        dist, prev = search(nodes, source)
        if dist[exit_node] < best:
            best = dist[exit_node]

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
        d = load_data("test_day12.txt")
        test_answer_1 = 31
        test_answer_2 = 29
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day12.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
