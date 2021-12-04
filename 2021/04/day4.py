from dataclasses import dataclass
from functools import cached_property
from itertools import chain
from typing import Iterable


@dataclass
class Board:
    grid: list[list[int]]
    already_won: bool = False

    @cached_property
    def winning_sets(self) -> list[set[int]]:
        sets = []
        for row in self.grid:
            sets.append(set(row))
        for i in range(len(self.grid)):
            sets.append(set(row[i] for row in self.grid))
        return sets

    @property
    def all_numbers(self) -> Iterable[int]:
        return chain.from_iterable(self.grid)

    def evaluate_win(self, called_numbers: set[int]) -> bool:
        won = any(win_set <= called_numbers for win_set in self.winning_sets)
        if won:
            self.already_won = True
        return won

    def calculate_score(self, called_numbers: set[int], winning_number: int) -> int:
        unmarked_sum = 0
        for num in self.all_numbers:
            if num not in called_numbers:
                unmarked_sum += num
        return unmarked_sum * winning_number


def get_numbers_and_boards(filename: str) -> tuple[list[int], list[Board]]:
    with open(filename, 'r') as file:
        lines = file.readlines()
        numbers = list(map(int, lines[0].split(",")))
        boards = []
        grid = None
        for line in lines[1:]:
            if not line.strip():
                if grid is not None:
                    boards.append(Board(grid))
                grid = []
            else:
                row = list(map(int, line.split()))
                grid.append(row)
        return numbers, boards


def get_first_winning_score(numbers: Iterable[int], boards: Iterable[Board]) -> int:
    called_numbers = set()
    for number in numbers:
        called_numbers.add(number)
        for board in boards:
            if board.evaluate_win(called_numbers):
                return board.calculate_score(called_numbers, number)


def get_last_winning_score(numbers: Iterable[int], boards: Iterable[Board]) -> int:
    called_numbers = set()
    last_winner_score = None
    for number in numbers:
        called_numbers.add(number)
        for board in boards:
            if not board.already_won and board.evaluate_win(called_numbers):
                last_winner_score = board.calculate_score(called_numbers, number)

    return last_winner_score


if __name__ == '__main__':
    numbers, boards = get_numbers_and_boards("input.txt")
    print(get_first_winning_score(numbers, boards))
    print(get_last_winning_score(numbers, boards))

    # 3724 too low