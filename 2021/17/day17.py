from math import sqrt, ceil
from typing import Optional


def does_probe_hit(vx: int, vy: int, target_x: tuple[int, int], target_y: tuple[int, int]) -> Optional[int]:
    x, y = 0, 0
    max_y = 0
    while True:
        if target_x[0] <= x <= target_x[1] and target_y[0] <= y <= target_y[1]:
            return max_y
        if x > target_x[1] or y < target_y[0]:
            return None

        x += vx
        y += vy

        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1

        vy -= 1
        if y > max_y:
            max_y = y


def get_starting_velocity(distance: int) -> int:
    """
    With drag of 1, probe will travel V + V-1 + V-2 + ... + 0, which is V(V+1)/2
    If we have the distance, we can use the quadratic formula to find starting velocity
    """
    return ceil((-1 + sqrt(1 + 8*distance)) / 2)


def find_max_y(target_x: tuple[int, int], target_y: tuple[int, int]) -> tuple[int, int]:
    velocity_pairs = set()
    vx_min = get_starting_velocity(target_x[0])
    vx_max = get_starting_velocity(target_x[1])
    print(vx_min, vx_max)

    max_y = 0
    for vx in range(vx_min, 1000):  # used vx_max for part 1, but let it rip for part 2
        for vy in range(-1000, 1000):
            y = does_probe_hit(vx, vy, target_x, target_y)
            if y is not None:
                # print(f"{vx} {vy} Reached {y}")
                max_y = max(y, max_y)
                velocity_pairs.add((vx, vy))

    return max_y, len(velocity_pairs)



if __name__ == '__main__':
    # assert does_probe_hit(7, 2, (20, 30), (-10, -5)) is not None
    # assert does_probe_hit(6, 3, (20, 30), (-10, -5)) is not None
    # assert does_probe_hit(9, 0, (20, 30), (-10, -5)) is not None
    # assert does_probe_hit(17, -4, (20, 30), (-10, -5)) is None
    # assert does_probe_hit(6, 9, (20, 30), (-10, -5)) == 45

    # print(does_probe_hit(21, 53, (230, 283), (-107, -57)))

    # print(find_max_y((20, 30), (-10, -5)))
    print(find_max_y((230, 283), (-107, -57)))
    # 1378 too low
    # 522 too low
