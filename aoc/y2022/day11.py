""" Day 11 Solutions """

from typing import List, Callable
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
class Monkey:
    """YOU'RE A MONKEY"""

    items: List
    operation: Callable
    test: Callable
    inspections: int = 0
    part_two: bool = False
    prime: int = 1
    primes = 1

    def inspect_item(self):
        self.inspections += 1
        value = self.items[0]
        del self.items[0]
        value = self.operation(value)
        if not self.part_two:
            value = value // 3
        else:
            value %= self.primes
        return value, self.test(value)


def parse_monkey(lines, part_two=False):
    """PARSE MONKEY PARSE!!!"""
    l, r = "".join(lines[0].split(" ")).split(":")
    items = ints(r.split(","))
    l, r = "".join(lines[1].split(" ")).split(":")
    function = f'lambda old: {r.split("=")[-1]}'
    # Shhh don't tell Greg
    operation = eval(function)  # pylint: disable=eval-used
    divis = int(lines[2].split(" ")[-1])
    if_true = int(lines[3].split(" ")[-1])
    if_false = int(lines[4].split(" ")[-1])
    test = lambda x: if_true if x % divis == 0 else if_false
    return Monkey(items=items, operation=operation, test=test, part_two=part_two, prime=divis)


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)

    # Part One:
    monkeys = []
    for step in range(0, len(d), 7):
        monkeys.append(parse_monkey(d[step + 1 : step + 7]))

    for _ in range(20):
        for monkey in monkeys:
            while monkey.items:
                value, throw_to = monkey.inspect_item()
                monkeys[throw_to].items.append(value)
    insp = [m.inspections for m in monkeys]
    insp = sorted(insp)
    result_1 = insp[-1] * insp[-2]

    # Part Two:
    monkeys = []
    for step in range(0, len(d), 7):
        monkeys.append(parse_monkey(d[step + 1 : step + 7], part_two=True))

    primes = [monkey.prime for monkey in monkeys]
    prime = int(np.prod(primes))
    for monkey in monkeys:
        monkey.primes = prime

    for _ in range(10000):
        for monkey in monkeys:
            while monkey.items:
                value, throw_to = monkey.inspect_item()
                monkeys[throw_to].items.append(value)
    insp = [m.inspections for m in monkeys]
    insp = sorted(insp)
    result_2 = insp[-1] * insp[-2]

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day11.txt")
        test_answer_1 = 10605
        test_answer_2 = 2713310158
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day11.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
