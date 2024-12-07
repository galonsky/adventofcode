import re
from collections import defaultdict
from typing import Generator, Iterable

RULE_PATTERN = re.compile(r'(\d+)\|(\d+)')


def get_rules(filename: str) -> Generator[tuple[int, int], None, None]:
    with open(filename, 'r') as file:
        for line in file:
            match = RULE_PATTERN.match(line.strip())
            if not match:
                return
            yield int(match.group(1)), int(match.group(2))


def get_updates(filename: str) -> Generator[list[int], None, None]:
    with open(filename, 'r') as file:
        for line in file:
            if ',' not in line:
                continue
            parts = line.split(',')
            yield [int(p) for p in parts]


def get_middle_if_correct(update: list[int], before_after: dict[int, set[int]]) -> int:
    seen = set()
    for n in update:
        after = before_after.get(n)
        if after and after & seen:
            return 0
        seen.add(n)
    return update[len(update) // 2]


def get_sum_middles(rules: Iterable[tuple[int, int]], updates: Iterable[list[int]]) -> int:
    before_to_after = defaultdict(set)
    for rule in rules:
        before_to_after[rule[0]].add(rule[1])

    return sum(get_middle_if_correct(update, before_to_after) for update in updates)


if __name__ == '__main__':
    rules = get_rules("input.txt")
    updates = get_updates("input.txt")
    print(get_sum_middles(rules, updates))