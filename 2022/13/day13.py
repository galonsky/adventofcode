import json
from functools import cmp_to_key
from itertools import chain
from typing import List, Generator, Iterable

PacketListType = List["PacketListType"] | int


def get_pairs(filename: str) -> Generator[tuple[PacketListType, PacketListType], None, None]:
    with open(filename, 'r') as file:
        line_iter = iter(file)
        while line := next(line_iter, None):
            line1 = line.strip()
            line2 = next(line_iter).strip()
            yield (json.loads(line1), json.loads(line2))
            next(line_iter, None)


def get_sum_pairs_in_order(pairs: Iterable[tuple[PacketListType, PacketListType]]) -> int:
    sum_in_order = 0
    for i, pairs in enumerate(pairs):
        res = cmp(*pairs)
        if res == -1:
            sum_in_order += (i + 1)
    return sum_in_order


def get_decoder_key(pairs: Iterable[tuple[PacketListType, PacketListType]]) -> int:
    all_packets = chain(chain.from_iterable(pairs), ([[2]], [[6]]))
    inorder = sorted(all_packets, key=cmp_to_key(cmp))
    return (inorder.index([[6]]) + 1) * (inorder.index([[2]]) + 1)


def cmp(left: PacketListType, right: PacketListType) -> int:
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        if right < left:
            return 1
        return 0

    if isinstance(left, list) and isinstance(right, list):
        for i in range(max(len(left), len(right))):
            try:
                lvalue = left[i]
            except IndexError:
                return -1
            try:
                rvalue = right[i]
            except IndexError:
                return 1
            res = cmp(lvalue, rvalue)
            if res != 0:
                return res
        return 0

    if isinstance(left, int):
        newleft = [left]
        return cmp(newleft, right)

    newright = [right]
    return cmp(left, newright)


def test_things():
    assert cmp([1,1,3,1,1], [1,1,5,1,1]) == -1
    assert cmp([[1],[2,3,4]], [[1],4]) == -1
    assert cmp([9], [[8,7,6]]) == 1
    assert cmp([[4,4],4,4], [[4,4],4,4,4]) == -1
    assert cmp([7,7,7,7], [7,7,7]) == 1
    assert cmp([], [3]) == -1
    assert cmp([[[]]], [[]]) == 1
    assert cmp([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9]) == 1


if __name__ == '__main__':
    pairs = list(get_pairs("input.txt"))
    print(get_sum_pairs_in_order(pairs))
    print(get_decoder_key(pairs))