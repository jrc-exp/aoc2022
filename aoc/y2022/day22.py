""" Day 22 Solutions """

from argparse import ArgumentParser
from collections import defaultdict
import re
import numpy as np

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


def build_edges_part_two(board, r, c):
    """build the board edges"""
    edges = dict()
    edges = defaultdict(lambda: defaultdict(lambda: None))
    face_locs = []
    if max([r, c]) == 16:
        h, w = 4, 4
    else:
        h, w = 50, 50
    for y in range(1, h * 4 + 1, h):
        for x in range(1, w * 4 + 1, w):
            if board.get((y, x)):
                face_locs.append((y // h, x // h))

    left = (-1, 0, 0)
    right = (1, 0, 0)
    front = (0, 1, 0)
    back = (0, -1, 0)
    top = (0, 0, 1)
    bottom = (0, 0, -1)
    if h == 4:
        face_rotations = {
            front: (face_locs[0], 0),
            top: (face_locs[1], 2),
            left: (face_locs[2], 1),
            bottom: (face_locs[3], 0),
            back: (face_locs[4], 2),
            right: (face_locs[5], 2),
        }
    else:
        face_rotations = {
            front: (face_locs[0], 0),
            right: (face_locs[1], 0),
            bottom: (face_locs[2], 0),
            left: (face_locs[3], 2),
            top: (face_locs[5], 3),
            back: (face_locs[4], 2),
        }
    faces = dict()
    for face, (offset, rotation) in face_rotations.items():
        grid = np.zeros((h, w), dtype=np.object)
        for y in range(1, h + 1):
            for x in range(1, w + 1):
                grid[y - 1, x - 1] = (offset[0] * h + y, offset[1] * h + x)
        grid = np.rot90(grid, k=-rotation)
        faces[face] = grid

    for x in range(1, c + 1):
        for y in range(1, r + 1):
            node = edges[(y, x)]
            for move in NEIGHBOR4:
                next_node = (y + move[0], x + move[1])
                if board.get(next_node):
                    node[move] = next_node

    top_slice = slice(0, 1, 1), slice(0, h, 1)
    bottom_slice = slice(h - 1, h, 1), slice(0, h, 1)
    left_slice = slice(0, h, 1), slice(0, 1, 1)
    right_slice = slice(0, h, 1), slice(h - 1, h, 1)

    slice_map = {U: top_slice, D: bottom_slice, L: left_slice, R: right_slice}

    lines = [
        (front, U, top, D, False),
        (front, L, left, R, False),
        (front, R, right, L, False),
        (front, D, bottom, U, False),
        (back, U, top, U, True),
        (back, L, right, R, False),
        (back, R, left, L, False),
        (back, D, bottom, D, True),
        (bottom, L, left, D, True),
        (bottom, R, right, D, False),
        (top, R, right, U, True),
        (top, L, left, U, False),
    ]

    def do_rev(x, do):
        if do:
            return reversed(x)
        return x

    exits = dict()
    for face1, d1, face2, d2, rev in lines:
        slice1 = slice_map[d1]
        slice2 = slice_map[d2]
        edge1 = faces[face1][slice1[0], slice1[1]].ravel()
        edge2 = do_rev(faces[face2][slice2[0], slice2[1]].ravel(), rev)
        for pt1, pt2 in zip(edge1, edge2):
            pt1 = tuple(pt1)
            pt2 = tuple(pt2)
            # rotate the starting direction to map oriented exit direction:
            first_dir = d1
            n_rot = face_rotations[face1][1]
            for _ in range(n_rot):
                first_dir = turns[first_dir][L]
            edges[pt1][first_dir] = pt2

            # calculate the exit direction:
            n_rot = face_rotations[face2][1] + 2
            exit_dir = d2
            for _ in range(n_rot):
                exit_dir = turns[exit_dir][L]
            exits[(pt1, pt2)] = exit_dir

            # do the same in revers:
            # rotate the starting direction to map oriented exit direction:
            first_dir = d2
            n_rot = face_rotations[face2][1]  # + 2 for 180
            for _ in range(n_rot):
                first_dir = turns[first_dir][L]
            edges[pt2][first_dir] = pt1

            # calculate the exit direction:
            n_rot = face_rotations[face1][1] + 2
            exit_dir = d1
            for _ in range(n_rot):
                exit_dir = turns[exit_dir][L]
            exits[(pt2, pt1)] = exit_dir

    for loc in board:
        if not board[loc]:
            continue
        for move in NEIGHBOR4:
            if edges[loc][move] is None:
                print(loc, move)

    start = 1, min(x for x in range(1, c + 1) if board[1, x])
    return edges, start, exits


def build_edges(board, r, c):
    """build the board edges"""
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

    start = (1, left_edges[0])
    return edges, start


def build_board(input_data, part=1):
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

    if part == 1:
        edges, start = build_edges(board, r, c)
        exits = None
    else:
        edges, start, exits = build_edges_part_two(board, r, c)

    moves = input_data[r + 1]
    real_moves = []
    dist = strip_ints(moves)
    for m in dist:
        idx = moves.index(str(m)) + len(str(m))
        direction = moves[idx : idx + 1]
        direction = dir_map.get(direction)
        real_moves.append((m, direction))
        moves = moves[idx + 1 :]

    facing = R

    return board, edges, real_moves, start, facing, exits


def solve_p1(d):
    """solve p1"""
    facing_char_map = {
        R: ">",
        D: "v",
        L: "<",
        U: "^",
    }
    board, edges, moves, start, facing, _ = build_board(d)
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
    return facing, board, visited, loc


def solve_p2(d):
    """solve p1"""
    facing_char_map = {
        R: ">",
        D: "v",
        L: "<",
        U: "^",
    }
    board, edges, moves, start, facing, exits = build_board(d, part=2)
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
            if (loc, dest) in exits:
                facing = exits[(loc, dest)]
            loc = dest
            visited[loc] = facing_char_map[facing]
            path.append(loc)
        if rotate is None:
            continue
        facing = turns[facing][rotate]
        visited[loc] = facing_char_map[facing]
    return facing, board, visited, loc


def solve(d):
    """actual solution with puzzle input"""
    result_1, result_2 = 0, 0

    facing_map = {
        R: 0,
        D: 1,
        L: 2,
        U: 3,
    }

    facing, board, visited, loc = solve_p1(d)
    r, c = loc
    password = 1000 * r + 4 * c + facing_map[facing]
    print_path(board, visited)
    result_1 = password

    facing, board, visited, loc = solve_p2(d)
    r, c = loc
    password = 1000 * r + 4 * c + facing_map[facing]
    print_path(board, visited)
    result_2 = password

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
        test_answer_2 = 5031
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
