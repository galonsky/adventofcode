from typing import Generator, Tuple


SCORE_BY_MOVE = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

GAME_SCORES = {
    ('A', 'X'): 3,
    ('A', 'Y'): 6,
    ('A', 'Z'): 0,
    ('B', 'X'): 0,
    ('B', 'Y'): 3,
    ('B', 'Z'): 6,
    ('C', 'X'): 6,
    ('C', 'Y'): 0,
    ('C', 'Z'): 3,
}


def get_strategy_guide(filename: str) -> Generator[Tuple[str, str], None, None]:
    with open(filename, 'r') as file:
        for line in file:
            yield tuple(line.strip().split())


def get_score(move: Tuple[str, str]) -> int:
    return SCORE_BY_MOVE[move[1]] + GAME_SCORES[move]


def get_total_score(filename: str) -> int:
    guide = get_strategy_guide(filename)
    return sum(get_score(move) for move in guide)


if __name__ == '__main__':
    print(get_total_score("input.txt"))