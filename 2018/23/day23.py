import re

PATTERN = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')

class Nanobot:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def in_range(self, other_bot):
        distance = abs(self.x - other_bot.x) + abs(self.y - other_bot.y) + abs(self.z - other_bot.z)
        return distance <= self.r

    def coord_in_range(self, x, y, z):
        distance = abs(self.x - x) + abs(self.y - y) + abs(self.z - z)
        return distance <= self.r

    def num_in_range(self, bots):
        return sum((1 for bot in bots if self.in_range(bot)))

    def left(self):
        return self.x - self.r

    def right(self):
        return self.x + self.r

    def up(self):
        return self.y + self.r

    def down(self):
        return self.y - self.r

    def above(self):
        return self.z + self.r

    def below(self):
        return self.z - self.r

    def __str__(self):
        return '({}, {}, {}) r={}'.format(self.x, self.y, self.z, self.r)

    def __eq__(self, other):
        return (self.x, self.y, self.z, self.r) == (other.x, other.y, other.z, other.r)


def get_nanobots(filename):
    with open(filename) as file:
        for line in file:
            match = PATTERN.match(line.rstrip('\n'))
            yield Nanobot(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)))


def get_num_in_range_of_strongest(filename):
    nanobots = list(get_nanobots(filename))
    strongest = max(nanobots, key=lambda bot: bot.r)
    return sum((1 for bot in nanobots if strongest.in_range(bot)))

def get_max_overlap(sequence):
    max_overlap = -1

    current_overlap = 0
    for point in sequence:
        current_overlap += point[1]
        if current_overlap > max_overlap:
            max_overlap = current_overlap

    starts = []
    ends = []
    current_overlap = 0
    for point in sequence:
        current_overlap += point[1]
        if current_overlap == max_overlap:
            starts.append(point[0])
        elif len(ends) < len(starts):
            ends.append(point[0])

    assert len(starts) == len(ends)
    for i in range(len(starts)):
        yield (starts[i], ends[i])

def get_bot_with_most_in_range(filename):
    nanobots = list(get_nanobots(filename))
    max_bot = max(nanobots, key=lambda bot: bot.num_in_range(nanobots))

    in_range = [bot for bot in nanobots if max_bot.in_range(bot)]
    max_in_range = len(in_range)

    # import ipdb
    # ipdb.set_trace()

    lefts = [bot.left() for bot in in_range if bot.left() >= max_bot.left()]
    # min_x = min(lefts, default=max_bot.left())

    rights = [bot.right() for bot in in_range if bot.right() <= max_bot.right()]
    # max_x = max(rights, default=max_bot.right())

    unders = [bot.down() for bot in in_range if max_bot.down() <= bot.down()]
    # min_y = min(unders, default=max_bot.down())

    overs = [bot.up() for bot in in_range if max_bot.up() >= bot.up()]
    # max_y = max(overs, default=max_bot.up())

    belows = [bot.below() for bot in in_range if max_bot.below() <= bot.below()]
    # min_z = min(belows, default=max_bot.below())

    aboves = [bot.above() for bot in in_range if max_bot.above() >= bot.above()]
    # max_z = max(aboves, default=max_bot.above())

    xs = sorted([(x, 1) for x in lefts] + [(x, -1) for x in rights])
    ys = sorted([(y, 1) for y in unders] + [(y, -1) for y in overs])
    zs = sorted([(z, 1) for z in belows] + [(z, -1) for z in aboves])
    return xs, ys, zs

    x_ranges = list(get_max_overlap(xs))
    y_ranges = list(get_max_overlap(ys))
    z_ranges = list(get_max_overlap(zs))

    return x_ranges, y_ranges, z_ranges

    # xs = [x[0] for x in xs]
    # ys = [y[0] for y in ys]
    # zs = [z[0] for z in zs]

    # candidates = {}

    # for x in xs:
    #     for y in ys:
    #         for z in zs:
    #             num_in_range = sum((1 for bot in in_range if bot.coord_in_range(x, y, z)))
    #             candidates[(x, y, z)] = num_in_range

    # max_in_range = max(candidates.values())
    # return min((abs(key[0]) + abs(key[1]) + abs(key[2]) for key in candidates.keys() if candidates[key] == max_in_range))

    candidates = {}
    for x_range in x_ranges:
        for x in range(x_range[0], x_range[1] + 1):
            for y_range in y_ranges:
                for y in range(y_range[0], y_range[1] + 1):
                    for z_range in z_ranges:
                        for z in range(z_range[0], z_range[1] + 1):
                            #print(x, y, z)
                            num_in_range = sum((1 for bot in in_range if bot.coord_in_range(x, y, z)))
                            candidates[(x, y, z)] = num_in_range
    max_in_range = max(candidates.values())
    return min((abs(key[0]) + abs(key[1]) + abs(key[2]) for key in candidates.keys() if candidates[key] == max_in_range))
    #return (max_bot.x, max_bot.y, max_bot.z), max_bot.num_in_range(nanobots)

print(get_bot_with_most_in_range('day23_sample2.txt'))