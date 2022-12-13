import dataclasses
from collections import deque
from functools import reduce
from heapq import nlargest
from operator import mul
from typing import Iterable, Iterator, Union, Optional


@dataclasses.dataclass
class MonkeyRule:
    id: int
    items: deque[int]
    operation: tuple[str, Union[int, str]]
    divisible: int
    true_monkey: int
    false_monkey: int
    num_items_inspected: int = 0

    def adjust_worry_level(self, worry_level: int, special_divisor: Optional[int]) -> int:
        if special_divisor is None:
            return worry_level // 3
        return worry_level % special_divisor

    def inspect(self, monkeys_by_id: dict[int, "MonkeyRule"], worry_reduction_advanced: bool = False) -> None:
        while self.items:
            worry_level = self.items.popleft()
            self.num_items_inspected += 1
            operand = self.operation[1] if isinstance(self.operation[1], int) else worry_level
            worry_level = (worry_level + operand) if self.operation[0] == "+" else (worry_level * operand)
            worry_level = self.adjust_worry_level(worry_level, special_divisor=reduce(mul, [rule.divisible for rule in monkeys_by_id.values()]) if worry_reduction_advanced else None)
            result = worry_level % self.divisible == 0
            new_monkey = self.true_monkey if result else self.false_monkey
            monkeys_by_id[new_monkey].items.append(worry_level)



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
                items=deque(items),
                operation=operation_tuple,
                divisible=divisible,
                true_monkey=true_monkey,
                false_monkey=false_monkey,
            )
            id += 1


def get_monkey_business(rules: Iterable[MonkeyRule], rounds: int, worry_reduction_advanced: bool = False) -> int:
    rules_by_id: dict[int, MonkeyRule] = {
        rule.id: rule for rule in rules
    }
    for _ in range(rounds):
        for monkey in rules_by_id.values():
            monkey.inspect(monkeys_by_id=rules_by_id, worry_reduction_advanced=worry_reduction_advanced)

    print([rule.num_items_inspected for rule in rules_by_id.values()])
    return reduce(mul, nlargest(2, [rule.num_items_inspected for rule in rules_by_id.values()]))



if __name__ == '__main__':
    monkeys = list(parse_monkeys("input.txt"))
    # print(get_monkey_business(monkeys, 20))
    print(get_monkey_business(monkeys, 10000, worry_reduction_advanced=True))