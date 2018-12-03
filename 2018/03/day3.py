import re
from collections import defaultdict

PATTERN = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

def get_lines(filename):
    with open(filename) as file:
        for line in file:
            yield line.rstrip('\n')


def get_key(x, y):
    return '{},{}'.format(x, y)


# part 1
def get_overlapped_inches(filename):
    taken_keys = defaultdict(int)
    for line in get_lines(filename):
        match = PATTERN.match(line)
        left = int(match.group(2))
        down = int(match.group(3))
        width = int(match.group(4))
        height = int(match.group(5))

        for x in range(left, left + width):
            for y in range(down, down + height):
                key = get_key(x, y)
                taken_keys[key] += 1
    return len([value for value in taken_keys.values() if value > 1])


# part 2
def get_only_untouched(filename):
    taken_keys = defaultdict(set)
    ids_to_keys = defaultdict(list)
    for line in get_lines(filename):
        match = PATTERN.match(line)
        id = int(match.group(1))
        left = int(match.group(2))
        down = int(match.group(3))
        width = int(match.group(4))
        height = int(match.group(5))

        for x in range(left, left + width):
            for y in range(down, down + height):
                key = get_key(x, y)
                taken_keys[key].add(id)
                ids_to_keys[id].append(key)
    for id, keys in ids_to_keys.items():
        key_sets = [taken_keys[key] for key in keys]
        if all(key_set == {id} for key_set in key_sets):
            return id


print(get_only_untouched('day3_input.txt'))

