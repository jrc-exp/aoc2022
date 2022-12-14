""" Day 14 Solutions """
from argparse import ArgumentParser
from copy import deepcopy


from aoc.y2022.utils import load_data


def ints(x):
    return list(map(int, x))


def occupied(grid, xp, yp):
    if xp < 0 or yp < 0 or yp >= len(grid) or xp >= len(grid[0]):
        return False
    if grid[yp][xp] in ["o", "#", "+"]:
        return True
    return False


D = [0, 1]
DL = [-1, 1]
DR = [+1, 1]
DIR = D, DL, DR

global minx, miny
minx, miny = 0, 0


def trans(x, y):
    return x - minx, y - miny


def drop_sand(grid, sand):
    """drop unit of sand"""
    x, y = trans(*sand)
    falling = True
    while falling:
        for d in DIR:
            xp, yp = x + d[0], y + d[1]
            if not occupied(grid, xp, yp):
                x, y = xp, yp
                break
        else:
            falling = False
        if x < 0 or y < 0 or y >= len(grid) or x >= len(grid[0]):
            return False
    grid[y][x] = "o"

    if trans(*sand) == (x, y):
        return False

    return True


def solve(d):
    """actual solution with puzzle input"""
    global minx, miny
    result_1, result_2 = 0, 0
    # print("INPUT DATA:")
    # print(d)
    sand = (500, 0)
    lines = []
    for row in d:
        xys = row.split(" -> ")
        parse = lambda x: ints(x.split(","))
        xys = list(map(parse, xys))
        lines.append(xys)
    maxx = max(max(x for xys in lines for (x, y) in xys), sand[0])
    minx = min(min(x for xys in lines for (x, y) in xys), sand[0])
    maxy = max(max(y for xys in lines for (x, y) in xys), sand[1])
    miny = min(min(y for xys in lines for (x, y) in xys), sand[1])
    # print(maxx, minx, maxy, miny)
    nr = maxy - miny + 1
    nc = maxx - minx + 1
    grid = [["." for _ in range(nc)] for _ in range(nr)]
    x, y = trans(*sand)
    grid[y][x] = "+"
    for line in lines:
        for idx in range(len(line) - 1):
            x1, y1 = trans(*line[idx])
            x2, y2 = trans(*line[idx + 1])
            if y1 == y2:
                xs = sorted([x1, x2])
                for x in range(xs[0], xs[1] + 1):
                    grid[y1][x] = "#"
            if x1 == x2:
                ys = sorted([y1, y2])
                for y in range(ys[0], ys[1] + 1):
                    grid[y][x1] = "#"

    def print_grid(grid):
        print()
        for idx, line in enumerate(grid):
            print(f"{idx:03d}", "".join(line))

    grid2 = deepcopy(grid)
    ct = 0
    while drop_sand(grid, sand):
        ct += 1
    print_grid(grid)

    result_1 = ct

    # Make a huger grid2:
    grid2.append(["." for _ in range(len(grid2[0]))])
    grid2.append(["#" for _ in range(len(grid2[0]))])
    extra = maxy - miny
    for idx, line in enumerate(grid2):
        if idx == len(grid2) - 1:
            extension = ["#" for _ in range(extra)]
        else:
            extension = ["." for _ in range(extra)]
        grid2[idx] = extension + grid2[idx] + extension
    minx -= extra

    print_grid(grid2)
    ct = 0
    while drop_sand(grid2, sand):
        ct += 1
    print_grid(grid2)

    result_2 = ct + 1

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day14.txt")
        test_answer_1 = 24
        test_answer_2 = 93
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day14.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
