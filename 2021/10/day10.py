from collections import deque
from typing import Iterable, Optional

CLOSING_TO_OPENING = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": '<',
}

CLOSING_TO_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def get_lines(filename: str) -> Iterable[str]:
    with open(filename) as file:
        for line in file:
            yield line.strip()


def get_error_score(line: str) -> int:
    stack = deque()
    for ch in line:
        if ch not in CLOSING_TO_OPENING:
            stack.append(ch)
        else:
            last_opener = stack.pop()
            if last_opener != CLOSING_TO_OPENING[ch]:
                return CLOSING_TO_SCORE[ch]
    return 0


def get_total_error_score(lines: Iterable[str]) -> int:
    return sum(get_error_score(line) for line in lines)


if __name__ == '__main__':
    print(get_total_error_score(get_lines("input.txt")))

