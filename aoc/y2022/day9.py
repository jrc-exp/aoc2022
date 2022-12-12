""" Day 9 Solutions """
from argparse import ArgumentParser
from dataclasses import dataclass
from aoc.y2022.utils import load_data


@dataclass
class RopeHead:
    """Rope Head"""

    x: int = 0
    y: int = 0

    def move(self, direction):
        if direction == "L":
            self.x -= 1
        if direction == "R":
            self.x += 1
        if direction == "U":
            self.y += 1
        if direction == "D":
            self.y -= 1


@dataclass
class RopeTail(RopeHead):
    """Rope Tail"""

    visited = None

    def __post_init__(self):
        self.visited = set()

    def follow(self, head):
        """Follow"""
        y_dist = head.y - self.y
        x_dist = head.x - self.x
        if abs(y_dist) == 2:
            self.y += y_dist // 2
            self.x = head.x
        elif abs(x_dist) == 2:
            self.x += x_dist // 2
            self.y = head.y
        self.visited.add((self.y, self.x))


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0
    print("INPUT DATA:")
    # print(d)
    head = RopeHead()
    tail = RopeTail()
    tails = [RopeTail() for _ in range(9)]

    for row in d:
        direction, ct = row.split(" ")
        ct = int(ct)
        for _ in range(ct):
            head.move(direction)
            tail.follow(head)
            for idx, t in enumerate(tails):
                if idx == 0:
                    t.follow(head)
                else:
                    t.follow(tails[idx - 1])
    result_1 = len(tail.visited)
    result_2 = len(tails[-1].visited)

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day9.txt")
        test_answer_1 = 13
        test_answer_2 = 1
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
        d = load_data("test_day9_2.txt")
        test_answer_1 = 88
        test_answer_2 = 36
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day9.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
