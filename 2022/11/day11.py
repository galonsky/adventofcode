import dataclasses
from typing import Iterable, Iterator, Union


@dataclasses.dataclass
class MonkeyRule:
    id: int
    starting_items: list[int]
    operation: tuple[str, Union[int, str]]
    divisible: int
    true_monkey: int
    false_monkey: int


def next_line(line_iter: Iterator[str]) -> str:
    return next(line_iter).strip()


def parse_monkeys(filename: str) -> Iterable[MonkeyRule]:
    with open(filename, 'r') as file:
        line_iter = iter(file)
        id = 0
        while next(line_iter, None):
            # monkey line, starting from 0
            starting_line = next_line(line_iter)
            parts = starting_line.split("Starting items: ")
            items = [int(part) for part in parts[1].split(", ")]
            operation_line = next_line(line_iter)
            parts = operation_line.split("Operation: new = old ")
            parts = parts[1].split()
            operation_tuple = parts[0], int(parts[1]) if parts[1].isnumeric() else parts[1]
            divisible_line = next_line(line_iter)
            parts = divisible_line.split("Test: divisible by ")
            divisible = int(parts[1])
            true_line = next_line(line_iter)
            true_monkey = int(true_line.split("If true: throw to monkey ")[1])
            false_line = next_line(line_iter)
            false_monkey = int(false_line.split("If false: throw to monkey ")[1])
            next(line_iter, None)  # blank
            yield MonkeyRule(
                id=id,
                starting_items=items,
                operation=operation_tuple,
                divisible=divisible,
                true_monkey=true_monkey,
                false_monkey=false_monkey,
            )
            id += 1


if __name__ == '__main__':
    monkeys = list(parse_monkeys("sample.txt"))
    print(monkeys)