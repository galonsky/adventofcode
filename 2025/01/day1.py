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


def get_password_2(rotations: Iterable[str]) -> int:
    current = 50
    num_zeroes = 0
    for rotation in rotations:
        direction = rotation[0]
        magnitude = int(rotation[1:])
        num_zeroes += magnitude // 100
        if direction == 'L':
            newval = (current - magnitude) % 100
            if current != 0:
                if newval == 0 or newval > current:
                    print("mid added")
                    num_zeroes += 1
        else:
            newval = (current + magnitude) % 100
            if current != 0:
                if newval == 0 or newval < current:
                    print("mid added")
                    num_zeroes += 1
        current = newval
        print(current)
    return num_zeroes


if __name__ == "__main__":
    # 6706 too high
    print(get_password_2(get_rotations("input.txt")))


