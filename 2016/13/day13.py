from enum import Enum


INPUT = 1352


class LocationType(Enum):
    OPEN = 0
    WALL = 1


def compute_location(x: int, y: int) -> LocationType:
    num = x*x + 3*x + 2*x*y + y + y*y + INPUT
    bin_rep = "{0:b}".format(num)
    num_ones = len([bit for bit in bin_rep if bit == "1"])
    return LocationType.OPEN if num_ones % 2 == 0 else LocationType.WALL


def print_map(max_x: int, max_y: int):
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            line += "X" if (x == 31 and y == 39) else "#" if compute_location(x, y) == LocationType.WALL else '.'
        print(line)


if __name__ == "__main__":
    print_map(40, 40)

