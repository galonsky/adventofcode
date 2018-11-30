COMPASS = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']


def compass_distance(a, b):
    return abs(COMPASS.index(a) - COMPASS.index(b))


def reverse(dir):
    index = (COMPASS.index(dir) + 4) % len(COMPASS)
    return COMPASS[index]


def net(moves):
    for direction in sorted(moves.keys(), key=moves.get, reverse=True):
        if moves[direction] > 0 and reverse(direction) in moves:
            moves[direction] = moves[direction] - moves[reverse(direction)]
            moves[reverse(direction)] = 0
    return {dir: moves[dir] for dir in moves if moves[dir] > 0}


def decompose(moves):
    keys = [key for key in moves.keys()]
    for direction in keys:
        if len(direction) == 2:
            half = moves[direction] // 2
            moves[direction] = 0
            moves[direction[0]] = moves.setdefault(direction[0], 0) + half
            moves[direction[1]] = moves.setdefault(direction[1], 0) + half
    return {dir: moves[dir] for dir in moves if moves[dir] > 0}


def calc_distance(moves):
    moves = net(moves)
    moves = decompose(moves)
    moves = net(moves)

    distance = sum(moves.values())
    print('{}: {}'.format(moves, distance))

    return distance


def get_distance():
    with open('day11_input.txt') as file:
        input = file.read()
        directions = input.split(',')
        moves = {}
        max = 0
        for direction in directions:
            if direction not in moves:
                moves[direction] = 1
            else:
                moves[direction] = moves[direction] + 1

            distance = calc_distance(dict(moves))
            if distance > max:
                max = distance

        return max


# netted:
# 410 nw
# 149 sw

# 149 "west"
# 261 nw

# 288 n

# 1w + 1n = 2nw

# 149 * 2 + 261 nw
# 139 n

# = 698

print(get_distance())
