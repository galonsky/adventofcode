import re
from typing import Tuple, Optional, Generator
from collections import deque

MOVE_PATTERN = re.compile(r'move (\d+) from (\d+) to (\d+)')
SAMPLE_CRATES = [  # top to bottom
    deque(["N", "Z"]),
    deque(["D", "C", "M"]),
    deque(["P"]),
]

INPUT_CRATES = [
    deque("CQB"),
    deque("ZWQR"),
    deque("VLRMB"),
    deque("WTVHZC"),
    deque("GVNBHZD"),
    deque("QVFJCPNH"),
    deque("SZWRTGD"),
    deque("PZQBNMGC"),
    deque("PFQWMBJN"),
]


def get_input(filename: str) -> Generator[Tuple[int, int, int], None, None]:
    with open(filename, 'r') as file:
        for line in file:
            match = MOVE_PATTERN.match(line)
            yield int(match.group(1)), int(match.group(2)), int(match.group(3))


def do_moves(filename: str, crates: list[deque[str]] = SAMPLE_CRATES) -> str:
    moves = get_input(filename)
    for move in moves:
        num, src, dest = move
        for _ in range(num):
            crates[dest-1].appendleft(crates[src-1].popleft())

    result = ""
    for crate in crates:
        result += crate.popleft()
    return result


if __name__ == '__main__':
    print(do_moves("input.txt", INPUT_CRATES))

