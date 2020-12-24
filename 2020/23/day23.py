from dataclasses import dataclass
from typing import Optional, Iterator, Dict, Tuple


@dataclass
class Cup:
    label: int
    next: Optional["Cup"] = None

    def __iter__(self) -> Iterator["Cup"]:
        return CupIterator(self)


class CupIterator(Iterator[Cup]):

    def __init__(self, start: Cup):
        self._start = start
        self._current = start
        self._first = True

    def __iter__(self) -> Iterator[Cup]:
        return self

    def __next__(self) -> Cup:
        if self._first:
            self._first = False
            return self._current
        _next = self._current.next
        if _next == self._start:
            raise StopIteration
        self._current = _next
        return _next



def build_circle(input: str) -> Cup:
    first_cup = Cup(label=int(input[0]))
    last = first_cup
    for i in range(1, len(input)):
        label = int(input[i])
        new_cup = Cup(label=label)
        last.next = new_cup
        last = new_cup
    last.next = first_cup
    return first_cup


def build_linked_dict(input: str) -> Tuple[int, Dict[int, int]]:
    linked_dict = {}
    first_cup = int(input[0])
    last = first_cup
    for i in range(1, len(input)):
        label = int(input[i])
        linked_dict[last] = label
        last = label
    linked_dict[last] = first_cup
    return first_cup, linked_dict


def part1():
    current, linked_dict = build_linked_dict("586439172")
    print(linked_dict)
    max_val = max(linked_dict.keys())
    for _ in range(100):
        picked_up = [
            linked_dict[current],
            linked_dict[linked_dict[current]],
            linked_dict[linked_dict[linked_dict[current]]],
        ]
        linked_dict[current] = linked_dict[picked_up[-1]]

        destination = current - 1
        while destination in picked_up and destination > 0:
            destination -= 1
        if destination == 0:
            destination = max_val
            while destination in picked_up and destination > 1:
                destination -= 1

        # next after destination
        gap_end = linked_dict[destination]
        linked_dict[destination] = picked_up[0]
        linked_dict[picked_up[-1]] = gap_end
        current = linked_dict[current]

    current = linked_dict[1]
    nums_after_one = ''
    while current != 1:
        nums_after_one += str(current)
        current = linked_dict[current]
    return nums_after_one


if __name__ == '__main__':
    print(part1())
