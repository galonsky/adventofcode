import re
from collections import defaultdict
from typing import Iterable

INITIAL_PATTERN = re.compile(r'value (\d+) goes to bot (\d+)')
RULE_PATTERN = re.compile(r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)')


def get_input(filename: str) -> Iterable[str]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip('\n')


def part1():
    lines = list(get_input('input.txt'))
    chips_by_bot = defaultdict(set)
    chips_by_output = defaultdict(set)
    rules = {}

    for line in lines:
        if match := INITIAL_PATTERN.match(line):
            value, bot = match.groups()
            chips_by_bot[int(bot)].add(int(value))
        elif match := RULE_PATTERN.match(line):
            bot, low_type, low_dest, high_type, high_dest = match.groups()
            rules[int(bot)] = (
                (low_type, int(low_dest)),
                (high_type, int(high_dest)),
            )
        else:
            raise Exception('unexpected!')

    bots_with_two_chips = {key for key in chips_by_bot.keys() if len(chips_by_bot[key]) == 2}
    while bots_with_two_chips:
        for bot in bots_with_two_chips:
            low_rules, high_rules = rules[bot]
            low = min(chips_by_bot[bot])
            high = max(chips_by_bot[bot])

            if low == 17 and high == 61:
                print(bot)
                return

            low_type, low_dest = low_rules
            if low_type == 'bot':
                chips_by_bot[low_dest].add(low)
            else:
                chips_by_output[low_dest].add(low)

            high_type, high_dest = high_rules
            if high_type == 'bot':
                chips_by_bot[high_dest].add(high)
            else:
                chips_by_output[high_dest].add(high)
            chips_by_bot[bot] = set()
        bots_with_two_chips = {key for key in chips_by_bot.keys() if len(chips_by_bot[key]) == 2}
    print(chips_by_output)


if __name__ == '__main__':
    part1()
