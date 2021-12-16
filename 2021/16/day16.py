from _operator import add
from dataclasses import dataclass
from functools import reduce
from itertools import islice
from typing import Iterator, Iterable


@dataclass
class BitSnapshot:
    hex_index: int
    bit_index: int


class HexBitwiseIterator(Iterator):
    def __init__(self, hex_string: str):
        self.hex_string = hex_string
        self.hex_index = 0
        self.bit_index = -1

    def __next__(self) -> int:
        if self.bit_index == 3:
            self.hex_index += 1
            self.bit_index = 0
        else:
            self.bit_index += 1

        if self.hex_index >= len(self.hex_string):
            raise StopIteration

        return (int(self.hex_string[self.hex_index], 16) >> (3 - self.bit_index)) & 1
        # hex_bits = bin(int(self.hex_string[self.hex_index], 16))[2:]
        # return int(hex_bits[self.bit_index])

    def __iter__(self) -> Iterator[int]:
        return self

    def finish_hex_digit(self) -> None:
        if self.bit_index != 3:
            self.hex_index += 1
            self.bit_index = 0

    def snapshot(self) -> BitSnapshot:
        return BitSnapshot(self.hex_index, self.bit_index)

    def num_bits_since(self, snapshot: BitSnapshot) -> int:
        return (self.hex_index - snapshot.hex_index) * 4 + self.bit_index - snapshot.bit_index


def bits_to_int(bits: Iterable[int]) -> int:
    return int(reduce(
        add, map(str, bits)
    ), 2)


def get_literal(bits: HexBitwiseIterator) -> int:
    bit_string = ""
    while True:
        prefix = next(bits)
        bit_string += "".join(map(str, islice(bits, 4)))
        if prefix == 0:
            bits.finish_hex_digit()
            return int(bit_string, 2)


def next_bits_to_int(bits: Iterator[int], n: int) -> int:
    n_bits = list(islice(bits, n))
    if not n_bits:
        raise StopIteration  # hacky but whatever
    return bits_to_int(n_bits)


def get_sum_of_versions(bit_iter: HexBitwiseIterator, max_bits: int = None, max_packets: int = None) -> int:
    sum_of_versions = 0
    num_packets = 0
    snapshot = bit_iter.snapshot()
    while True:
        try:
            version = next_bits_to_int(bit_iter, 3)
        except StopIteration:
            return sum_of_versions
        sum_of_versions += version
        type_id = next_bits_to_int(bit_iter, 3)
        # print(version)
        # print(type_id)
        if type_id == 4:
            literal = get_literal(bit_iter)
            # print(literal)
        else:
            length_type_id = next(bit_iter)
            if length_type_id == 0:
                data_length = next_bits_to_int(bit_iter, 15)
                sum_of_versions += get_sum_of_versions(bit_iter, max_bits=data_length)
            else:
                num_subpackets = next_bits_to_int(bit_iter, 11)
                sum_of_versions += get_sum_of_versions(bit_iter, max_packets=num_subpackets)
        num_packets += 1
        if num_packets == max_packets or bit_iter.num_bits_since(snapshot) == max_bits:
            return sum_of_versions


def get_sum(hex_string: str) -> int:
    bit_iter = HexBitwiseIterator(hex_string)
    return get_sum_of_versions(bit_iter)


if __name__ == '__main__':
    # assert get_sum("8A004A801A8002F478") == 16
    assert get_sum("620080001611562C8802118E34") == 12
    # assert get_sum("C0015000016115A2E0802F182340") == 23
    # assert get_sum("A0016C880162017C3686B18A3D4780") == 31
