""" Day 21 Solutions """
import operator
import sympy as sym
from argparse import ArgumentParser
from collections import defaultdict


from aoc.y2022.utils import load_data

op_map = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def ints(x):
    return list(map(int, x))


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    waiting_for = defaultdict(list)
    monkeys = dict()
    values = dict()
    values_str = dict()
    unsolved = set()
    for row in d:
        monkey, formula = row.split(":")
        out = formula.lstrip(" ").split(" ")
        if len(out) == 1:
            values[monkey] = int(out[0])
            values_str[monkey] = int(out[0])
            if monkey == "humn":
                values_str[monkey] = "humn"
        else:
            a, op, b = out
            monkeys[monkey] = (op_map[op], a, b, op)
            waiting_for[a].append(monkey)
            waiting_for[b].append(monkey)
            unsolved.add(monkey)

    while unsolved:
        for monkey in unsolved:
            op, a, b, op_str = monkeys[monkey]
            if a in values and b in values:
                values[monkey] = op(values[a], values[b])
                if monkey == "root":
                    try:
                        values_str[monkey] = str(op(int(values_str[a]), int(values_str[b])))
                    except Exception:
                        values_str[monkey] = f"({values_str[a]}{op_str}{values_str[b]})"
                    result_1 = values[monkey]
                    humn = sym.Symbol("humn")
                    a, b = eval(values_str[a]), eval(values_str[b])
                    answer = sym.solveset(a - b, humn)
                    result_2 = list(answer)[0]
                    return int(result_1), int(result_2)
                else:
                    values_str[monkey] = f"({values_str[a]}{op_str}{values_str[b]})"

    return int(result_1), int(result_2)


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day21.txt")
        test_answer_1 = 152
        test_answer_2 = 301
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day21.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
