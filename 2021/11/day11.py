from collections import deque
from typing import Iterable


VECTORS = (
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
    (1, 1),
    (1, -1),
    (-1, -1),
    (-1, 1),
)


def get_octopi(filename: str) -> Iterable[list[int]]:
    with open(filename, 'r') as file:
        for line in file:
            yield [int(ch) for ch in line.strip()]


def process_step(octopi: list[list[int]]) -> int:
    flashed: set[tuple[int, int]] = set()
    for y, row in enumerate(octopi):
        for x, energy in enumerate(row):
            new_energy = energy + 1
            octopi[y][x] = new_energy
            if new_energy > 9:
                flashed.add((x, y))
    new_flashes = deque(flashed)
    while new_flashes:
        x, y = new_flashes.pop()
        for dx, dy in VECTORS:
            newx = x + dx
            newy = y + dy
            if 0 <= newy < len(octopi) and 0 <= newx < len(octopi[0]):
                octopi[newy][newx] += 1
                if (newx, newy) not in flashed and octopi[newy][newx] > 9:
                    flashed.add((newx, newy))
                    new_flashes.appendleft((newx, newy))
    for x, y in flashed:
        octopi[y][x] = 0

    for row in octopi:
        print("".join(map(str, row)))
    print()
    return len(flashed)


def get_total_flashes(octopi: list[list[int]], n: int) -> int:
    return sum(process_step(octopi) for _ in range(n))


def get_first_step_all_flashes(octopi: list[list[int]]) -> int:
    n = 1
    while True:
        num_flashes = process_step(octopi)
        if num_flashes == len(octopi) * len(octopi[0]):
            return n
        n += 1


if __name__ == '__main__':
    octopi = list(get_octopi("input.txt"))
    # print(get_total_flashes(octopi, 100))
    print(get_first_step_all_flashes(octopi))