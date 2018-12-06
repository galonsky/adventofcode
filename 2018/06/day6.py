from collections import defaultdict

def get_lines(filename):
    with open(filename) as file:
        for line in file:
            yield line.rstrip('\n')


def get_manhattan_distance(x0, y0, x1, y1):
    return abs(x0 - x1) + abs(y0 - y1)


def get_areas(filename):
    plot = defaultdict(dict)
    xs = []
    ys = []
    for i, line in enumerate(get_lines(filename)):
        parts = line.split(', ')
        x = int(parts[0])
        y = int(parts[1])
        xs.append(x)
        ys.append(y)
    x_min = min(xs)
    x_max = max(xs)
    y_min = min(ys)
    y_max = max(ys)

    num_coords = len(xs)
    areas_by_id = defaultdict(int)
    infinites = set()
    ten_thousand_range_count = 0
    
    for x in range(x_min - 1, x_max + 2):
        for y in range(y_min - 1, y_max + 2):
            distance_id_tuples = [(get_manhattan_distance(x, y, xs[i], ys[i]), i) for i in range(num_coords)]
            distance_sum = sum(map(lambda a: a[0], distance_id_tuples))
            if distance_sum < 10000:
                ten_thousand_range_count += 1
            distance_id_tuples.sort()
            if len(distance_id_tuples) < 2 or distance_id_tuples[0][0] != distance_id_tuples[1][0]:
                first = distance_id_tuples[0]
                areas_by_id[first[1]] += 1
                plot[x][y] = first[1]

                if x == x_min - 1 or x == x_max + 1 or y == y_min - 1 or y == y_max + 1:
                    infinites.add(first[1])
            else:
                plot[x][y] = '.'


    max_area = 0
    for i in range(num_coords):
        if i in infinites:
            continue
        max_area = max(max_area, areas_by_id.get(i, 0))
    return max_area, ten_thousand_range_count

print(get_areas('day6_input.txt'))
