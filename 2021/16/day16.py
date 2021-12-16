from typing import Iterator


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

        if self.hex_index == len(self.hex_string):
            raise StopIteration

        return (int(self.hex_string[self.hex_index], 16) >> (3 - self.bit_index)) & 1
        # hex_bits = bin(int(self.hex_string[self.hex_index], 16))[2:]
        # return int(hex_bits[self.bit_index])

    def __iter__(self) -> Iterator[int]:
        return self


if __name__ == '__main__':
    iterator = HexBitwiseIterator("AB")
    print(list(iterator))