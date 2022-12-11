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


def get_num_locations_tail_visited(instructions: Iterable[Tuple[str, int]], num_knots: int) -> int:
    knots = [(0, 0) for _ in range(num_knots)]

    unique_tail_locations = set()
    unique_tail_locations.add(knots[-1])

    for instruction in instructions:
        vector = VECTORS_BY_DIRECTION[instruction[0]]
        for _ in range(instruction[1]):
            knots[0] = (knots[0][0] + vector[0], knots[0][1] + vector[1])

            for i in range(1, len(knots)):
                if are_touching(knots[i-1], knots[i]):
                    continue

                if knots[i] == (knots[i-1][0] + 2, knots[i-1][1]):
                    # tail is to the right
                    knots[i] = (knots[i][0] - 1, knots[i][1])
                elif knots[i] == (knots[i-1][0] - 2, knots[i-1][1]):
                    # tail is to the left
                    knots[i] = (knots[i][0] + 1, knots[i][1])
                elif knots[i] == (knots[i-1][0], knots[i-1][1] + 2):
                    # tail is above
                    knots[i] = (knots[i][0], knots[i][1] - 1)
                elif knots[i] == (knots[i-1][0], knots[i-1][1] - 2):
                    # tail is below
                    knots[i] = (knots[i][0], knots[i][1] + 1)
                elif knots[i-1][0] - knots[i][0] > 0 and knots[i-1][1] - knots[i][1] > 0:
                    # head is northeast
                    knots[i] = (knots[i][0] + 1, knots[i][1] + 1)
                elif knots[i-1][0] - knots[i][0] < 0 and knots[i-1][1] - knots[i][1] > 0:
                    # head is northwest
                    knots[i] = (knots[i][0] - 1, knots[i][1] + 1)
                elif knots[i-1][0] - knots[i][0] > 0 and knots[i-1][1] - knots[i][1] < 0:
                    # head is southeast
                    knots[i] = (knots[i][0] + 1, knots[i][1] - 1)
                elif knots[i-1][0] - knots[i][0] < 0 and knots[i-1][1] - knots[i][1] < 0:
                    # head is southwest
                    knots[i] = (knots[i][0] - 1, knots[i][1] - 1)

            unique_tail_locations.add(knots[-1])
    return len(unique_tail_locations)


if __name__ == '__main__':
    instructions = get_instructions("input.txt")
    print(get_num_locations_tail_visited(instructions, 2))
    instructions = get_instructions("input.txt")
    print(get_num_locations_tail_visited(instructions, 10))