""" Day 7 Solutions """

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

    children = defaultdict(list)
    parents = dict()
    sizes = dict()
    total_sizes = dict()
    dirs = set(["/"])
    base_nodes = []
    pwd = ""
    idx = 0
    do_ls = False
    base_node = False
    pwd = "/"
    for row in d[1:]:
        if row.startswith("$"):
            if do_ls and base_node:
                base_nodes.append(pwd)
                total_sizes[pwd] = sum(sizes[a] for a in children[pwd])
            do_ls = False
        if row.startswith("$ cd"):
            new_dir = row.split(" ")[-1]
            if new_dir == "..":
                pwd = parents[pwd]
            else:
                if pwd == "/":
                    pwd = pwd + new_dir
                else:
                    pwd = pwd + "/" + new_dir
            continue
        if row.startswith("$ ls"):
            do_ls = True
            base_node = True
            continue
        if do_ls:
            case, name = row.split(" ")
            if pwd == "/":
                name = pwd + name
            else:
                name = pwd + "/" + name
            if name in sizes:
                print("You're fucked!", name)
            if case == "dir":
                dirs.add(name)
                parents[name] = pwd
                sizes[name] = 0
                base_node = False
            else:
                parents[name] = pwd
                sizes[name] = int(case)
            children[pwd].append(name)

    def full_path(d):
        path = ""
        while d in parents:
            path = parents[d] + "/" + path
            d = parents[d]
        return path

    def size(d):
        if d in total_sizes:
            return total_sizes[d]
        if d in dirs:
            return sum(size(a) for a in children[d])
        return sizes[d]

    all_sizes = [size(d) for d in reversed(list(dirs))]
    result_1 = sum(sorted(list(filter(lambda x: x <= 100000, all_sizes))))

    free_space = 70000000 - size("/")
    req_free_space = 30000000
    req_del_size = req_free_space - free_space

    print(req_del_size)

    matching_sizes = list(sorted(filter(lambda x: x >= req_del_size, all_sizes)))
    print(matching_sizes)

    result_2 = matching_sizes[0]

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day7.txt")
        test_answer_1 = 95437
        test_answer_2 = 24933642
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day7.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
