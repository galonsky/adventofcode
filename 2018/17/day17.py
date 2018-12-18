import re
from collections import defaultdict
from collections import deque

PATTERN = re.compile(r'([xy])=(\d+),\s+([xy])=(\d+)\.\.(\d+)')

def build_scan(filename):
    scan = defaultdict(lambda: defaultdict(lambda: '.'))
    max_y = 0
    with open(filename) as file:
        for line in file:
            match = PATTERN.match(line.rstrip('\n'))
            if match.group(1) == 'x':
                x = int(match.group(2))
                for y in range(int(match.group(4)), int(match.group(5)) + 1):
                    scan[x][y] = '#'
                    if y > max_y:
                        max_y = y
            else:
                y = int(match.group(2))
                for x in range(int(match.group(4)), int(match.group(5)) + 1):
                    scan[x][y] = '#'
                if y > max_y:
                        max_y = y
    scan[500][0] = '+'
    return scan, max_y

def print_scan(scan, max_y):
    min_x = min(scan.keys())
    max_x = max(scan.keys())
    for y in range(max_y + 1):
        for x in range(min_x, max_x + 1):
            print(scan[x][y], end='')
        print()
    print()


queued_calls = deque()

def waterfall_file(filename):
    scan, max_y = build_scan(filename)
    #print_scan(scan, max_y)
    waterfall(scan, 500, 0, max_y)
    while True:
        if not queued_calls:
            break
        call = queued_calls.pop()
        waterfall(scan, call[0], call[1], max_y)

    print_scan(scan, max_y)
    return count_water_tiles(scan)


def count_water_tiles(scan):
    count = 0
    for x, y_map in scan.items():
        for y, c in y_map.items():
            # this 3 is hardcoded for my input. (min_y)
            if y >= 3 and (c == '~' or c == '|'):
                count += 1
    return count



def waterfall(scan, x, y, max_y, x_lambda=None):
    # import ipdb
    # ipdb.set_trace()
    if y > max_y:
        return
    this = scan[x][y]
    if this == '#':
        return x
    if this =='~':
        return False
    below = scan[x][y+1]
    if below == '.':
        if this != '+':
            scan[x][y] = '|'
        #print_scan(scan, max_y)
        waterfall(scan, x, y+1, max_y)
        return False

    below = scan[x][y+1]

    if below == '|':
        scan[x][y] = '|'
        return False
    if below == '#' or below == '~':
        scan[x][y] = '|'
        #print_scan(scan, max_y)
        if x_lambda:
            return waterfall(scan, x_lambda(x), y, max_y, x_lambda)
        else:
            left_index = waterfall(scan, x-1, y, max_y, lambda x: x-1)
            right_index = waterfall(scan, x+1, y, max_y, lambda x: x+1)
            if left_index is not False and right_index is not False:
                for x_i in range(left_index + 1, right_index):
                    scan[x_i][y] = '~'
                for x_i in range(left_index + 1, right_index):
                    if scan[x_i][y-1] == '|':
                        # waterfall(scan, x_i, y-1, max_y)
                        queued_calls.appendleft((x_i, y-1))

    return False


print(waterfall_file('day17_input.txt'))