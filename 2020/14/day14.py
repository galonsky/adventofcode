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


def recursive_replace_floating_vals(mask: str, address: int) -> Iterable[int]:
    index = mask.find('X')
    if index == -1:
        yield address
        return

    new_mask = mask.replace('X', '0', 1)  # doesn't matter what, just need to get rid of X
    one_mask = 1 << (35 - index)
    yield from recursive_replace_floating_vals(new_mask, address | one_mask)
    yield from recursive_replace_floating_vals(new_mask, address & ~one_mask)


def mask_address(mask: str, address: int) -> Iterable[int]:
    masked_address = address | int(mask.replace('X', '0'), 2)
    yield from recursive_replace_floating_vals(mask, masked_address)


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


def part2():
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
            addresses = mask_address(mask_str, loc)
            for address in addresses:
                mem[address] = val
    return sum([
        val for val in mem.values() if val != 0
    ])


if __name__ == '__main__':
    print(part2())
