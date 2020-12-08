import re, pprint
from collections import defaultdict
from typing import Iterable, Dict, List, Tuple, Set

CONTENT_PATTERN = re.compile(r'(\d+) (.*)')


def get_rules(filename: str) -> Iterable[str]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip('.\n')


def get_rule_map(filename: str) -> Dict[str, List[Tuple[str, int]]]:
    contents_by_bag = defaultdict(list)
    for rule in get_rules(filename):
        if rule.endswith('no other bags'):
            continue
        parts = rule.split(' contain ')
        container = parts[0].rstrip('s')
        rest = parts[1]
        contents = rest.split(', ')
        for content in contents:
            match = CONTENT_PATTERN.match(content)
            num, target = match.groups()
            contents_by_bag[container].append((target.rstrip('s'), int(num)))
    return contents_by_bag


def get_all_contents(bag_name: str, rule_map: Dict[str, List[Tuple[str, int]]]) -> Set[str]:
    stuff_in_this_bag = set(pair[0] for pair in rule_map.get(bag_name, []))
    total_children = set(stuff_in_this_bag)
    for child in stuff_in_this_bag:
        total_children |= get_all_contents(child, rule_map)
    return total_children


def part1():
    rule_map = get_rule_map('input.txt')
    total_with_gold = 0
    for bag in rule_map:
        contents = get_all_contents(bag, rule_map)
        if 'shiny gold bag' in contents:
            total_with_gold += 1
    print(total_with_gold)

if __name__ == '__main__':
    part1()