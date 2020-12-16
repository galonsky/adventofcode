from collections import defaultdict, deque
from functools import reduce
from typing import Iterable, Deque


def get_turns_apart(turns: Deque[int]) -> int:
    iterator = reversed(turns)
    return abs(reduce(lambda a, b: a-b, [next(iterator) for _ in range(2)]))


def play_game(starting_nums: Iterable[int], num_turns: int) -> int:
    memory = defaultdict(deque)  # most recent at the right side
    i = 0
    last_num = 0
    for num in starting_nums:
        memory[num].append(i)
        i += 1
        last_num = num

    for i in range(i, num_turns):
        if len(memory[last_num]) == 1:
            # speaks 0
            memory[0].append(i)
            last_num = 0
        else:
            last_num = get_turns_apart(memory[last_num])
            memory[last_num].append(i)

    return last_num


if __name__ == '__main__':
    print(play_game([14,3,1,0,9,5], 30000000))

