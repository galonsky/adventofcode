from collections import deque
from typing import Iterable


INPUT = [
1,1,1,1,1,5,1,1,1,5,1,1,3,1,5,1,4,1,5,1,2,5,1,1,1,1,3,1,4,5,1,1,2,1,1,1,2,4,3,2,1,1,2,1,5,4,4,1,4,1,1,1,4,1,3,1,1,1,2,1,1,1,1,1,1,1,5,4,4,2,4,5,2,1,5,3,1,3,3,1,1,5,4,1,1,3,5,1,1,1,4,4,2,4,1,1,4,1,1,2,1,1,1,2,1,5,2,5,1,1,1,4,1,2,1,1,1,2,2,1,3,1,4,4,1,1,3,1,4,1,1,1,2,5,5,1,4,1,4,4,1,4,1,2,4,1,1,4,1,3,4,4,1,1,5,3,1,1,5,1,3,4,2,1,3,1,3,1,1,1,1,1,1,1,1,1,4,5,1,1,1,1,3,1,1,5,1,1,4,1,1,3,1,1,5,2,1,4,4,1,4,1,2,1,1,1,1,2,1,4,1,1,2,5,1,4,4,1,1,1,4,1,1,1,5,3,1,4,1,4,1,1,3,5,3,5,5,5,1,5,1,1,1,1,1,1,1,1,2,3,3,3,3,4,2,1,1,4,5,3,1,1,5,5,1,1,2,1,4,1,3,5,1,1,1,5,2,2,1,4,2,1,1,4,1,3,1,1,1,3,1,5,1,5,1,1,4,1,2,1
]


def get_num_fish(timers: Iterable[int], num_days: int) -> int:
    current_fish = deque(timers)

    for _ in range(num_days):
        new_fish = deque()
        while current_fish:
            timer = current_fish.popleft()
            if timer == 0:
                new_fish.append(6)
                new_fish.append(8)
            else:
                new_fish.append(timer - 1)
        current_fish = new_fish
    return len(current_fish)


def get_num_children(starting_timer: int, num_days: int) -> int:
    """
    3
    2
    1
    0
    6   6
    5   5
    4   4
    3   3
    2   2
    1   1
    0   0
    6   6   6   6

    double every day = 2^x
    double ever 6 days = 2 ^ (x / 6)




    3
    2
    1
    0
    6   8
    5   7
    4   6
    3   5
    2   4
    1   3
    0   2
    6   1   8
    5   0   7
    4   6   6   8
    3   5   5   7
    2   4   4   6
    1   3   3   5
    0   2   2   4
    6   1   1   3   8
    5   0   0   2   7
    4   6   6   1   6   8
    3   5   5   0   5   7
    2   4   4   6   4   6   8
    1   3   3   5   3   5   7
    0   2   2   4   2   4   6
    6   1   1   3   1   3   5   8
    5   0   0   2   0   2   4   7
    4   6   6   1   6   1   3   6   8   8   8
    3   5   5   0   5   0   2   5   7   7   7
    2   4   4   6   4   6   1   4   6   6   6   8   8
    1   3   3   5   3   5   0   3   5   5   5   7   7
    0   2   2   4   2   4   6   2   4   4   4   6   6   8


    N = 3
    0: 0
    1: 0
    2: 0
    3: 0
    4: 1

    fish of timer N will produce ~ N // 7 direct descendents

    """


if __name__ == '__main__':
    print(get_num_fish([3], 256))
