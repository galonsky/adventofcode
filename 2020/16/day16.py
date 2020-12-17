from dataclasses import dataclass
from typing import List, Iterable


@dataclass
class Interval:
    min: int
    max: int

    @classmethod
    def from_str(cls, interval: str) -> 'Interval':
        parts = interval.strip().split('-')
        return cls(min=int(parts[0]), max=int(parts[1]))

    def test(self, val: int) -> bool:
        return self.min <= val <= self.max


@dataclass
class Rule:
    field: str
    intervals: List[Interval]

    @classmethod
    def from_str(cls, rule: str) -> 'Rule':
        parts = rule.split(':')
        field = parts[0]
        intervals = parts[1].split(' or ')

        return Rule(
            field=field,
            intervals=[Interval.from_str(inv) for inv in intervals]
        )

    def test_val(self, val: int) -> bool:
        return any(
            interval.test(val) for interval in self.intervals
        )


def get_rules(filename: str) -> Iterable[Rule]:
    with open(filename, 'r') as file:
        for line in file:
            yield Rule.from_str(line)


def get_nearby_tickets(filename: str) -> Iterable[List[int]]:
    with open(filename, 'r') as file:
        for line in file:
            nums = line.split(',')
            yield [int(num) for num in nums]


def part1():
    rules = list(get_rules('input_rules.txt'))
    tickets = get_nearby_tickets('input_nearby.txt')
    # for rule in rules:
    #     print(rule)

    total_invalid = 0

    for ticket in tickets:
        for val in ticket:
            if any(
                rule.test_val(val) for rule in rules
            ):
                continue
            else:
                # print(val)
                total_invalid += val
    return total_invalid


if __name__ == '__main__':
    print(part1())