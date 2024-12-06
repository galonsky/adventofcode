from typing import Generator

from pandas import DataFrame
import numpy as np


XMAS = ['X', 'M', 'A', 'S']
SAMX = list(reversed(XMAS))


def get_word_search(filename: str) -> list[str]:
    with open(filename, 'r') as file:
        return [line.strip() for line in file]


def get_all_4_by_4(ws: list[str]) -> Generator[DataFrame, None, None]:
    height = len(ws)
    width = len(ws[0])
    for y in range(height - 3):
        for x in range(width - 3):
            yield DataFrame([list(ws[y+i][x:x+4]) for i in range(4)])


def get_all_rows(df: DataFrame) -> Generator[list[str], None, None]:
    for _, row in df.iterrows():
        yield row.tolist()
    for _, row in df.T.iterrows():
        yield row.tolist()
    yield np.diagonal(df.to_numpy()).tolist()
    yield np.fliplr(df.to_numpy()).diagonal().tolist()


def row_matches(row: list[str]) -> int:
    return 1 if row == XMAS or row == SAMX else 0


def find_num_matches(ws: list[str]) -> int:
    subsets = get_all_4_by_4(ws)
    total = 0
    for subset in subsets:
        print(subset)
        matches = sum(row_matches(row) for row in get_all_rows(subset))
        print("num matches: {}".format(str(matches)))
        total += matches
    return total



if __name__ == '__main__':
    ws = get_word_search("example.txt")
    print(find_num_matches(ws))
