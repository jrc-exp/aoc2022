""" Day 2 Solutions """

import sys
from argparse import ArgumentParser
from collections import Counter, defaultdict
from itertools import permutations, product

import numpy as np

from aoc.y2022.utils import load_data


def ints(x):
    return list(map(int, x))


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    print(d)
    MAP = {
        "A": "Rock",
        "B": "Paper",
        "C": "Scissors",
        "X": "Rock",
        "Y": "Paper",
        "Z": "Scissors",
    }
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    LOSE = 0
    TIE = 3
    WIN = 6
    SCORE = {
        "Rock": ROCK,
        "Paper": PAPER,
        "Scissors": SCISSORS,
    }
    OUTCOME = {
        ("Rock", "Rock"): TIE,
        ("Rock", "Paper"): WIN,
        ("Rock", "Scissors"): LOSE,
        ("Paper", "Rock"): LOSE,
        ("Paper", "Paper"): TIE,
        ("Paper", "Scissors"): WIN,
        ("Scissors", "Rock"): WIN,
        ("Scissors", "Paper"): LOSE,
        ("Scissors", "Scissors"): TIE,
    }

    def score(a, b):
        return SCORE[b] + OUTCOME[(a, b)]

    result_1 = sum(score(MAP[v[0]], MAP[v[2]]) for v in d)

    MAP_GOAL = {
        "X": LOSE,
        "Y": TIE,
        "Z": WIN,
    }

    def score2(a, b):
        b = DESIRED_OUTCOME[(a, b)]
        return SCORE[b] + OUTCOME[(a, b)]

    DESIRED_OUTCOME = {
        ("Rock", TIE): "Rock",
        ("Rock", WIN): "Paper",
        ("Rock", LOSE): "Scissors",
        ("Paper", LOSE): "Rock",
        ("Paper", TIE): "Paper",
        ("Paper", WIN): "Scissors",
        ("Scissors", WIN): "Rock",
        ("Scissors", LOSE): "Paper",
        ("Scissors", TIE): "Scissors",
    }
    result_2 = sum(score2(MAP[v[0]], MAP_GOAL[v[2]]) for v in d)
    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day2.txt")
        test_answer_1 = 15
        test_answer_2 = 12
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day2.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
