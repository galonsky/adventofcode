from typing import Generator, Tuple


def _to_tuple(elf: str) -> Tuple[int, int]:
    parts = elf.split("-")
    return int(parts[0]), int(parts[1])


def get_assignments(filename: str) -> Generator[Tuple[Tuple[int, int], Tuple[int, int]], None, None]:
    with open(filename, 'r') as file:
        for line in file:
            elves = line.strip().split(",")
            yield _to_tuple(elves[0]), _to_tuple(elves[1])


def how_many_pairs_fully_contain(filename: str) -> int:
    assignments = get_assignments(filename)
    num_contained = 0
    for assignment in assignments:
        # first inside second
        if assignment[0][0] >= assignment[1][0] and assignment[0][1] <= assignment[1][1]:
            num_contained += 1
        # second inside first
        elif assignment[1][0] >= assignment[0][0] and assignment[1][1] <= assignment[0][1]:
            num_contained += 1
    return num_contained


if __name__ == '__main__':
    print(how_many_pairs_fully_contain("input.txt"))