from dataclasses import dataclass
from typing import Optional, Iterator


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


def part1():
    current = build_circle("586439172")
    # nums = [cur.label for cur in current]
    for _ in range(100):
        picked_up = [
            current.next,
            current.next.next,
            current.next.next.next,
        ]
        current.next = picked_up[-1].next
        looking_for = current.label - 1
        nums_below = [cup for cup in current if cup.label <= looking_for]
        destination = max(nums_below, key=lambda cup: cup.label) if nums_below else max(current, key=lambda cup: cup.label)
        gap_end = destination.next
        destination.next = picked_up[0]
        picked_up[-1].next = gap_end

        current = current.next

    while current.label != 1:
        current = current.next
    current = current.next
    return ''.join(str(cup.label) for cup in current)[:-1]


if __name__ == '__main__':
    print(part1())
