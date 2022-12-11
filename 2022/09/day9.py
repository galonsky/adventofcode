from typing import Generator, Tuple, Iterable


VECTORS_BY_DIRECTION: dict[str, tuple[int, int]] = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0),
}


def get_instructions(filename: str) -> Generator[Tuple[str, int], None, None]:
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            yield parts[0], int(parts[1])


def are_touching(head: tuple[int, int], tail: tuple[int, int]) -> bool:
    return abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1


def get_num_locations_tail_visited(instructions: Iterable[Tuple[str, int]]) -> int:
    head = (0, 0)
    tail = head

    unique_tail_locations = set()
    unique_tail_locations.add(tail)

    for instruction in instructions:
        vector = VECTORS_BY_DIRECTION[instruction[0]]
        for _ in range(instruction[1]):
            head = (head[0] + vector[0], head[1] + vector[1])

            if are_touching(head, tail):
                continue

            if tail == (head[0] + 2, head[1]):
                # tail is to the right
                tail = (tail[0] - 1, tail[1])
            elif tail == (head[0] - 2, head[1]):
                # tail is to the left
                tail = (tail[0] + 1, tail[1])
            elif tail == (head[0], head[1] + 2):
                # tail is above
                tail = (tail[0], tail[1] - 1)
            elif tail == (head[0], head[1] - 2):
                # tail is below
                tail = (tail[0], tail[1] + 1)
            elif head[0] - tail[0] > 0 and head[1] - tail[1] > 0:
                # head is northeast
                tail = (tail[0] + 1, tail[1] + 1)
            elif head[0] - tail[0] < 0 and head[1] - tail[1] > 0:
                # head is northwest
                tail = (tail[0] - 1, tail[1] + 1)
            elif head[0] - tail[0] > 0 and head[1] - tail[1] < 0:
                # head is southeast
                tail = (tail[0] + 1, tail[1] - 1)
            elif head[0] - tail[0] < 0 and head[1] - tail[1] < 0:
                # head is southwest
                tail = (tail[0] - 1, tail[1] - 1)

            unique_tail_locations.add(tail)
    return len(unique_tail_locations)


if __name__ == '__main__':
    instructions = get_instructions("input.txt")
    print(get_num_locations_tail_visited(instructions))