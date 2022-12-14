from typing import Generator, Tuple, Iterable


def get_input(filename: str) -> Generator[list[Tuple[int, int]], None, None]:
    with open(filename, 'r') as file:
        for line in file:
            pairs_list = []
            pairs = line.strip().split(" -> ")
            for pair in pairs:
                parts = pair.split(",")
                pairs_list.append((int(parts[0]), int(parts[1])))
            yield pairs_list


def build_map(lines: Iterable[list[Tuple[int, int]]]) -> dict[tuple[int, int], str]:
    sand_map: dict[tuple[int, int], str] = {}
    for line in lines:
        sand_map[line[0]] = "#"
        last = line[0]
        for i in range(1, len(line)):
            current = line[i]
            sand_map[current] = "#"
            if current[0] == last[0]:
                # vertical
                increment = 1 if current[1] - last[1] > 0 else -1
                for j in range(last[1] + increment, current[1], increment):
                    sand_map[(current[0], j)] = "#"
            else:
                # horizontal
                increment = 1 if current[0] - last[0] > 0 else -1
                for j in range(last[0] + increment, current[0], increment):
                    sand_map[(j, current[1])] = "#"
            last = current

    return sand_map


def print_map(sand_map: dict[tuple[int, int], str]) -> None:
    min_y = 0
    max_y = max(k[1] for k in sand_map)
    min_x = min(k[0] for k in sand_map)
    max_x = max(k[0] for k in sand_map)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            ch = sand_map.get((x, y), '.')
            print(ch, end="")
        print()


class OverTheEdgeException(Exception):
    pass


def drop_single_sand(sand_map: dict[tuple[int, int], str], lower_limit: int):
    sand = (500, 0)
    sand_map[sand] = '.'
    while True:
        below = (sand[0], sand[1] + 1)
        if below in sand_map:
            lower_left = (sand[0] - 1, sand[1] + 1)
            if lower_left in sand_map:
                lower_right = (sand[0] + 1, sand[1] + 1)
                if lower_right in sand_map:
                    # at rest
                    return
                else:
                    del sand_map[sand]
                    sand = lower_right
                    sand_map[sand] = '.'
            else:
                del sand_map[sand]
                sand = lower_left
                sand_map[sand] = '.'
        else:
            del sand_map[sand]
            sand = below
            sand_map[sand] = '.'
        if sand[1] > lower_limit:
            raise OverTheEdgeException


class AccessorWithFloor:
    def __init__(self, sand_map: dict[tuple[int, int], str], floor: int):
        self.sand_map = sand_map
        self.floor = floor

    def is_occupied(self, coord: tuple[int, int]) -> bool:
        if coord in self.sand_map:
            return True
        if coord[1] >= self.floor:
            return True
        return False

    def set(self, coord: tuple[int, int]) -> None:
        self.sand_map[coord] = 'o'

    def free(self, coord: tuple[int, int]) -> None:
        del self.sand_map[coord]


def drop_single_sand_with_floor(sand_map: dict[tuple[int, int], str], floor: int):
    accessor = AccessorWithFloor(sand_map, floor)
    sand = (500, 0)
    accessor.set(sand)
    while True:
        below = (sand[0], sand[1] + 1)
        if accessor.is_occupied(below):

            lower_left = (sand[0] - 1, sand[1] + 1)
            if accessor.is_occupied(lower_left):
                lower_right = (sand[0] + 1, sand[1] + 1)
                if accessor.is_occupied(lower_right):
                    # at rest
                    if sand == (500, 0):
                        raise OverTheEdgeException
                    return
                else:
                    accessor.free(sand)
                    sand = lower_right
                    accessor.set(sand)
            else:
                accessor.free(sand)
                sand = lower_left
                accessor.set(sand)
        else:
            accessor.free(sand)
            sand = below
            accessor.set(sand)
        # print()
        # print_map(sand_map)



def drop_all_sand(sand_map: dict[tuple[int, int], str]) -> int:
    max_y = max(k[1] for k in sand_map)
    num_at_rest = 0
    while True:
        try:
            drop_single_sand(sand_map, lower_limit=max_y)
            print_map(sand_map)
            num_at_rest += 1
        except OverTheEdgeException:
            return num_at_rest


def drop_all_sand_with_floor(sand_map: dict[tuple[int, int], str]) -> int:
    max_y = max(k[1] for k in sand_map)
    num_at_rest = 0
    while True:
        try:
            drop_single_sand_with_floor(sand_map, floor=max_y+2)
            num_at_rest += 1
        except OverTheEdgeException:
            return num_at_rest + 1


if __name__ == '__main__':
    lines = get_input("input.txt")
    sand_map = build_map(lines)
    print_map(sand_map)
    # print(drop_all_sand(sand_map))
    print(drop_all_sand_with_floor(sand_map))
