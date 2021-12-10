from collections import deque
from typing import Iterable, Optional

CLOSING_TO_OPENING = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": '<',
}


OPENING_TO_CLOSING = {v: k for k, v in CLOSING_TO_OPENING.items()}

CLOSING_TO_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


CLOSING_TO_COMPLETION_SCORE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
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


def get_completion_string(line: str) -> Optional[str]:
    stack = deque()
    for ch in line:
        if ch not in CLOSING_TO_OPENING:
            stack.append(ch)
        else:
            last_opener = stack.pop()
            if last_opener != CLOSING_TO_OPENING[ch]:
                return None

    comp_str = ""
    while stack:
        comp_str += OPENING_TO_CLOSING[stack.pop()]
    return comp_str


def get_total_error_score(lines: Iterable[str]) -> int:
    return sum(get_error_score(line) for line in lines)


def get_completion_score(completion_str: str) -> int:
    score = 0
    for ch in completion_str:
        score *= 5
        score += CLOSING_TO_COMPLETION_SCORE[ch]
    return score


def get_median_completion_score(lines: Iterable[str]) -> int:
    comp_strs = [get_completion_string(line) for line in lines]
    scores = sorted([get_completion_score(comp) for comp in comp_strs if comp is not None])
    return scores[len(scores) // 2]


if __name__ == '__main__':
    # print(get_total_error_score(get_lines("input.txt")))
    # print(get_completion_string("{([(<{}[<>[]}>{[]{[(<()>"))
    print(get_median_completion_score(get_lines("input.txt")))

