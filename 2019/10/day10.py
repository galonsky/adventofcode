def get_input(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines


def get_num_visible(asteroids, vantage_x, vantage_y):
    visible = 0
    seen_angles = set()
    for y in range(len(asteroids)):
        for x in range(len(asteroids[0])):
            if asteroids[y][x] != '#':
                continue
            if x == vantage_x and y == vantage_y:
                continue
            angle = (y - vantage_y) / (x - vantage_x)
            seen_angles.add(angle)
    return len(seen_angles)


def find_best_location(filename):
    asteroids = get_input(filename)
    # print(asteroids)
    num_visible_by_coordinate = {}
    for y in range(len(asteroids)):
        for x in range(len(asteroids[0])):
            num_visible_by_coordinate[(x, y)] = get_num_visible(asteroids, x, y)
    return max(num_visible_by_coordinate.values())

print(find_best_location('sample1.txt'))