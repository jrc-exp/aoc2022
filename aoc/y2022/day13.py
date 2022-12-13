""" Day 13 Solutions """

from argparse import ArgumentParser
from itertools import zip_longest
from functools import cmp_to_key

from aoc.y2022.utils import load_data


def compare(a, b):
    """Compare packets!"""
    if a is None and b is not None:
        return True
    if a is not None and b is None:
        return False
    if a is None and b is None:
        return None
    if isinstance(a, int) and isinstance(b, int):
        if a == b:
            return None
        return a < b
    if isinstance(a, int) and isinstance(b, list):
        return compare([a], b)
    if isinstance(a, list) and isinstance(b, int):
        return compare(a, [b])
    for c, d in zip_longest(a, b):
        result = compare(c, d)
        if result is None:
            continue
        return result


def custom_compare(a, b):
    out = compare(a, b)
    if out is None:
        return 0
    if out:
        return -1
    return 1


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    step = 3
    size = 2

    idx = 0
    correct = []
    all_packets = [[[2]], [[6]]]
    for offset in range(0, len(d), step):
        idx += 1
        l, r = list(map(eval, d[offset : offset + size]))
        all_packets.append(l)
        all_packets.append(r)

        if compare(l, r):
            correct.append(idx)

    result_1 = sum(correct)

    all_packets = sorted(all_packets, key=cmp_to_key(custom_compare))

    result_2 = (all_packets.index([[2]]) + 1) * (all_packets.index([[6]]) + 1)

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day13.txt")
        test_answer_1 = 13
        test_answer_2 = 140
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day13.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
