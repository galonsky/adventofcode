DIRECTION_TO_VECTOR: list[tuple[int, int]] = [
    (0, -1), # n
    (1, 0), #e
    (0, 1), # s
    (-1, 0), #w
]


def get_map(filename: str) -> list[str]:
    with open(filename, 'r') as file:
        return [line.strip() for line in file]


def get_starting(lab_map: list[str]) -> tuple[int, int]:
    for y, line in enumerate(lab_map):
        for x, ch in enumerate(line):
            if ch == '^':
                return x, y
    raise Exception("can't find!")


def get_num_unique_locations(lab_map: list[str]) -> int:
    locations = set()
    start_coords = get_starting(lab_map)
    height = len(lab_map)
    width = len(lab_map[0])
    x, y = start_coords
    direction = 0
    while 0 <= x < width and 0 <= y < height:
        locations.add((x, y))
        ahead = (x + DIRECTION_TO_VECTOR[direction][0], y + DIRECTION_TO_VECTOR[direction][1])
        if ahead[0] < 0 or ahead[0] >= width or ahead[1] < 0 or ahead[1] >= height:
            break
        if lab_map[ahead[1]][ahead[0]] == '#':
            direction = (direction + 1) % 4
            ahead = (x + DIRECTION_TO_VECTOR[direction][0], y + DIRECTION_TO_VECTOR[direction][1])
        x, y = ahead

    return len(locations)


if __name__ == '__main__':
    lab_map = get_map("input.txt")
    print(get_num_unique_locations(lab_map))
