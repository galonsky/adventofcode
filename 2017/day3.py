import math


def spiral_distance(n):
    root = math.ceil(math.sqrt(n))
    ring = root // 2
    side_len = ring * 2 + 1
    ring_index = n - (max(side_len - 2, 0) ** 2 + 1)
    first_axis = max(ring - 1, 0)
    dist_from_axis = abs((ring_index % max(side_len - 1, 1)) - first_axis)
    print('N: {}, Ring: {}, Side length: {}, Ring Index :{}, Dist from axis: {}'
          .format(n, ring, side_len, ring_index, dist_from_axis))
    return ring + dist_from_axis


def key(x, y):
    return ','.join((str(x), str(y)))

def set_with_sum_of_neighbors(spiral, x, y):
    sum = 0
    sum += spiral.get(key(x + 1, y), 0)
    sum += spiral.get(key(x - 1, y), 0)
    sum += spiral.get(key(x, y + 1), 0)
    sum += spiral.get(key(x, y - 1), 0)
    sum += spiral.get(key(x + 1, y + 1), 0)
    sum += spiral.get(key(x + 1, y - 1), 0)
    sum += spiral.get(key(x - 1, y + 1), 0)
    sum += spiral.get(key(x - 1, y - 1), 0)

    spiral[key(x, y)] = sum
    return sum

def iterate_spiral():
    spiral = {}
    spiral[key(0, 0)] = 1
    spiral[key(1, 0)] = 1
    x = 1
    y = 0
    cur = 3
    side = 2
    while True:


        # last iteration has gone one extra right
        # need to go up
        for i in range(side - 1):
            y += 1
            val = set_with_sum_of_neighbors(spiral, x, y)
            if val > 312051:
                print(val)
                return

            # spiral[key(x, y)] = cur
            # cur += 1
        for i in range(side):
            x -= 1
            val = set_with_sum_of_neighbors(spiral, x, y)
            if val > 312051:
                print(val)
                return
            # spiral[key(x, y)] = cur
            # cur += 1
        for i in range(side):
            y -= 1
            val = set_with_sum_of_neighbors(spiral, x, y)
            if val > 312051:
                print(val)
                return
            # spiral[key(x, y)] = cur
            # cur += 1
        side += 2
        for i in range(side - 1):
            x += 1
            val = set_with_sum_of_neighbors(spiral, x, y)
            if val > 312051:
                print(val)
                return
            # spiral[key(x, y)] = cur
            # cur += 1




iterate_spiral()
#print(spiral_distance(312051))
