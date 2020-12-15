import re
from typing import Iterable


MEM_PATTERN = re.compile(r'mem\[(\d+)] = (\d+)')


def get_lines(filename: str) -> Iterable[str]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip('\n')


def mask_val(mask: str, val: int) -> int:
    zeroes = int(mask.replace('X', '1'), 2)
    ones = int(mask.replace('X', '0'), 2)
    return (val & zeroes) | ones


def part1():
    mask_str = ''
    mem = {}
    lines = get_lines('input.txt')
    for line in lines:
        if line.startswith('mask'):
            mask_str = line[7:]
        else:
            match = MEM_PATTERN.match(line)
            loc = int(match.group(1))
            val = int(match.group(2))
            mem[loc] = mask_val(mask_str, val)
    return sum([
        val for val in mem.values() if val != 0
    ])


if __name__ == '__main__':
    print(part1())
