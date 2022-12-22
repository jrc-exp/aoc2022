""" Day 22 Solutions """

from argparse import ArgumentParser
from collections import defaultdict
import re

from aoc.y2022.utils import load_data, NEIGHBOR4, U, D, L, R

U, D = D, U


def strip_ints(x):
    return ints(re.findall("-?[0-9]+", x))


def ints(x):
    return list(map(int, x))


WALL = 2
SPACE = 1
char_map = {
    " ": 0,
    ".": 1,
    "#": 2,
}
rev_char_map = {
    0: " ",
    1: ".",
    2: "#",
}
dir_map = {
    "R": R,
    "L": L,
    "U": U,
    "D": D,
}
turns = {
    R: {
        L: U,
        R: D,
    },
    L: {
        L: D,
        R: U,
    },
    U: {
        L: L,
        R: R,
    },
    D: {
        L: R,
        R: L,
    },
}


def print_board(board):
    """
    Print the board
    """
    printing = True
    y = 0
    x = 0
    while printing and (y + 1, x + 1) in board:
        y += 1
        row = ""
        while printing:
            x += 1
            if (y, x) in board:
                row = row + rev_char_map[board[(y, x)]]
            else:
                printing = False
        printing = True
        x = 0
        print("".join(row))


def print_path(board, visited):
    """
    Print the path along the board
    """
    printing = True
    y = 0
    x = 0
    while printing and (y + 1, x + 1) in board:
        y += 1
        row = ""
        while printing:
            x += 1
            if (y, x) in visited:
                row = row + visited[(y, x)]
            elif (y, x) in board:
                row = row + rev_char_map[board[(y, x)]]
            else:
                printing = False
        printing = True
        x = 0
        print("".join(row))


def build_board(input_data):
    """parse the input and setup the board"""
    board = dict()
    for y, row in enumerate(input_data):
        if not row:
            break
        for x, char in enumerate(row):
            board[(y + 1, x + 1)] = char_map[char]

    r = max(y for (y, _) in board)
    c = max(x for (_, x) in board)
    for y in range(1, r + 1):
        for x in range(1, c + 1):
            if (y, x) not in board:
                board[(y, x)] = 0

    edges = dict()
    left_edges = []
    right_edges = []
    top_edges = []
    bottom_edges = []
    for y in range(1, r + 1):
        for x in range(1, c + 1):
            if board[(y, x)]:
                left_edges.append(x)
                break
        for x in range(c, 0, -1):
            if board[(y, x)]:
                right_edges.append(x)
                break
    for x in range(1, c + 1):
        for y in range(1, r + 1):
            if board[(y, x)]:
                top_edges.append(y)
                break
        for y in range(r, 0, -1):
            if board[(y, x)]:
                bottom_edges.append(y)
                break

    edges = defaultdict(lambda: defaultdict(lambda: None))
    for x in range(1, c + 1):
        for y in range(1, r + 1):
            node = edges[(y, x)]
            for move in NEIGHBOR4:
                next_node = (y + move[0], x + move[1])
                if board.get(next_node):
                    node[move] = next_node
                elif move is R:
                    node[R] = (y, left_edges[y - 1])
                elif move is L:
                    node[L] = (y, right_edges[y - 1])
                elif move is U:
                    node[U] = (bottom_edges[x - 1], x)
                elif move is D:
                    node[D] = (top_edges[x - 1], x)

    moves = input_data[r + 1]
    real_moves = []
    dist = strip_ints(moves)
    for m in dist:
        idx = moves.index(str(m)) + len(str(m))
        direction = moves[idx : idx + 1]
        direction = dir_map.get(direction)
        real_moves.append((m, direction))
        moves = moves[idx + 1 :]

    start = (1, left_edges[0])

    facing = R

    return board, edges, real_moves, start, facing


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0

    facing_char_map = {
        R: ">",
        D: "v",
        L: "<",
        U: "^",
    }
    board, edges, moves, start, facing = build_board(d)
    loc = start
    path = [
        loc,
    ]
    visited = dict()
    visited[loc] = facing_char_map[facing]
    for dist, rotate in moves:
        for _ in range(dist):
            dest = edges[loc][facing]
            if board[dest] == WALL:
                break
            loc = dest
            visited[loc] = facing_char_map[facing]
            path.append(loc)
        if rotate is None:
            continue
        facing = turns[facing][rotate]
        visited[loc] = facing_char_map[facing]

    r, c = loc
    facing_map = {
        R: 0,
        D: 1,
        L: 2,
        U: 3,
    }
    password = 1000 * r + 4 * c + facing_map[facing]
    print_path(board, visited)
    result_1 = password

    return result_1, result_2


def main():
    """Main function"""
    args = ArgumentParser()
    args.add_argument("--skip", action="store_true")
    args = args.parse_args()
    # load data:
    if not args.skip:
        print("**** TEST DATA ****")
        d = load_data("test_day22.txt")
        test_answer_1 = 6032
        test_answer_2 = 0
        test_solution_1, test_solution_2 = solve(d)
        assert test_solution_1 == test_answer_1, f"TEST #1 FAILED: TRUTH={test_answer_1}, YOURS={test_solution_1}"
        assert test_solution_2 == test_answer_2, f"TEST #2 FAILED: TRUTH={test_answer_2}, YOURS={test_solution_2}"
        print("**** TESTS PASSED ****")
        print("Test Answer 1: ", test_answer_1)
        print("My Test Answer 1: ", test_solution_1)
        print("Test Answer 2: ", test_answer_2)
        print("My Test Answer 2: ", test_solution_2)
    print("**** REAL DATA ****")
    d = load_data("day22.txt")
    answer_1, answer_2 = solve(d)
    print("Answer 1:", answer_1)
    print("Answer 2:", answer_2)


if __name__ == "__main__":
    main()
