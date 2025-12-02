from typing import *

def get_rotations(filename: str) -> Generator[str, None, None]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()

def get_password(rotations: Iterable[str]) -> int:
    current = 50
    num_zeroes = 0
    for rotation in rotations:
        direction = rotation[0]
        if direction == 'L':
            current -= int(rotation[1:])
        else:
            current += int(rotation[1:])
        if current % 100 == 0:
            num_zeroes += 1
    return num_zeroes


if __name__ == "__main__":
    print(get_password(get_rotations("input.txt")))


