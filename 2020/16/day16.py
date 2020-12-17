from dataclasses import dataclass
from functools import reduce
from pprint import pp
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

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Rule) and self.field == o.field

    def __hash__(self) -> int:
        return hash(self.field)


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


def is_ticket_valid(ticket: List[int], rules: List[Rule]) -> bool:
    for val in ticket:
        if not any(
                rule.test_val(val) for rule in rules
        ):
            return False
    return True


def part2():
    rules = list(get_rules('input_rules.txt'))
    tickets = list(get_nearby_tickets('input_nearby.txt'))

    valid_tickets = [ticket for ticket in tickets if is_ticket_valid(ticket, rules)]
    possible_rules_by_field_index = {}
    for i in range(len(valid_tickets[0])):
        possible_rules_by_field_index[i] = set(rules)

    for ticket in valid_tickets:
        for i, val in enumerate(ticket):
            for rule in rules:
                if not rule.test_val(val):
                    possible_rules_by_field_index[i].remove(rule)

    visited_indicies = set()
    index_by_rule = {}

    while len(visited_indicies) < len(possible_rules_by_field_index):
        index, rule_set = [pair for pair in possible_rules_by_field_index.items() if pair[0] not in visited_indicies and len(pair[1]) == 1][0]
        rule = next(iter(rule_set))
        index_by_rule[rule] = index
        # remove rule from all other indices
        for i in possible_rules_by_field_index:
            if i == index:
                continue
            try:
                possible_rules_by_field_index[i].remove(rule)
            except KeyError:
                pass
            visited_indicies.add(index)

    pp(possible_rules_by_field_index)
    my_ticket = [73,167,113,61,89,59,191,103,67,83,163,109,101,71,97,151,107,79,157,53]

    return reduce(
        lambda a, b: a*b,
        map(
            lambda rule: my_ticket[index_by_rule[rule]],
            filter(
                lambda rule: rule.field.startswith('departure'),
                index_by_rule,
            ),
        ),
    )


if __name__ == '__main__':
    print(part2())
