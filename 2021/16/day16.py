from _operator import add
from functools import reduce
from itertools import islice
from typing import Iterator, Iterable


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
        self.hex_index += 1
        self.bit_index = 0


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



def get_sum_of_versions(hex_string: str) -> int:
    bit_iter = HexBitwiseIterator(hex_string)
    while True:
        version = bits_to_int(islice(bit_iter, 3))
        type_id = bits_to_int(islice(bit_iter, 3))
        print(version)
        print(type_id)
        if type_id == 4:
            literal = get_literal(bit_iter)
            print(literal)
        else:
            raise NotImplementedError
        return


if __name__ == '__main__':
    get_sum_of_versions("D2FE28")