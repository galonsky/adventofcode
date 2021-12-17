from _operator import add
from dataclasses import dataclass
from functools import reduce
from itertools import islice
from typing import Iterator, Iterable

INPUT = "020D78804D397973DB5B934D9280CC9F43080286957D9F60923592619D3230047C0109763976295356007365B37539ADE687F333EA8469200B666F5DC84E80232FC2C91B8490041332EB4006C4759775933530052C0119FAA7CB6ED57B9BBFBDC153004B0024299B490E537AFE3DA069EC507800370980F96F924A4F1E0495F691259198031C95AEF587B85B254F49C27AA2640082490F4B0F9802B2CFDA0094D5FB5D626E32B16D300565398DC6AFF600A080371BA12C1900042A37C398490F67BDDB131802928F5A009080351DA1FC441006A3C46C82020084FC1BE07CEA298029A008CCF08E5ED4689FD73BAA4510C009981C20056E2E4FAACA36000A10600D45A8750CC8010989716A299002171E634439200B47001009C749C7591BD7D0431002A4A73029866200F1277D7D8570043123A976AD72FFBD9CC80501A00AE677F5A43D8DB54D5FDECB7C8DEB0C77F8683005FC0109FCE7C89252E72693370545007A29C5B832E017CFF3E6B262126E7298FA1CC4A072E0054F5FBECC06671FE7D2C802359B56A0040245924585400F40313580B9B10031C00A500354009100300081D50028C00C1002C005BA300204008200FB50033F70028001FE60053A7E93957E1D09940209B7195A56BCC75AE7F18D46E273882402CCD006A600084C1D8ED0E8401D8A90BE12CCF2F4C4ADA602013BC401B8C11360880021B1361E4511007609C7B8CA8002DC32200F3AC01698EE2FF8A2C95B42F2DBAEB48A401BC5802737F8460C537F8460CF3D953100625C5A7D766E9CB7A39D8820082F29A9C9C244D6529C589F8C693EA5CD0218043382126492AD732924022CE006AE200DC248471D00010986D17A3547F200CA340149EDC4F67B71399BAEF2A64024B78028200FC778311CC40188AF0DA194CF743CC014E4D5A5AFBB4A4F30C9AC435004E662BB3EF0"


@dataclass
class BitSnapshot:
    hex_index: int
    bit_index: int


class HexBitwiseIterator(Iterator):
    def __init__(self, hex_string: str):
        self.hex_string = hex_string
        self.hex_index = 0
        self.bit_index = 0

    def __next__(self) -> int:
        if self.hex_index >= len(self.hex_string):
            raise StopIteration

        ret_val = (int(self.hex_string[self.hex_index], 16) >> (3 - self.bit_index)) & 1

        if self.bit_index == 3:
            self.hex_index += 1
            self.bit_index = 0
        else:
            self.bit_index += 1

        return ret_val

    def __iter__(self) -> Iterator[int]:
        return self

    def snapshot(self) -> BitSnapshot:
        return BitSnapshot(self.hex_index, self.bit_index)

    def num_bits_since(self, snapshot: BitSnapshot) -> int:
        return (self.hex_index - snapshot.hex_index) * 4 + self.bit_index - snapshot.bit_index


def bits_to_int(bits: Iterable[int]) -> int:
    return int(reduce(
        add, map(str, bits)
    ), 2)
# EEEEEEEE00000000DDDD44440000CCCC888822223333000066660000
# 11101110000000001101010000001100100000100011000001100000
# VVVTTTILLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBCCCCCCCCCCC
def get_literal(bits: HexBitwiseIterator) -> int:
    bit_string = ""
    while True:
        prefix = next(bits)
        bit_string += "".join(map(str, islice(bits, 4)))
        if prefix == 0:
            # bits.finish_hex_digit()
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
            sum_of_versions += version
            type_id = next_bits_to_int(bit_iter, 3)
            # print(version)
            # print(type_id)
            if type_id == 4:
                literal = get_literal(bit_iter)
                print(literal)
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
        except StopIteration:
            return sum_of_versions


def get_sum(hex_string: str) -> int:
    bit_iter = HexBitwiseIterator(hex_string)
    return get_sum_of_versions(bit_iter)


if __name__ == '__main__':
    # assert "".join(map(str, HexBitwiseIterator("D2FE28"))) == "110100101111111000101000"
    # assert "".join(map(str, HexBitwiseIterator("38006F45291200"))) == "00111000000000000110111101000101001010010001001000000000"
    # assert "".join(
    #     map(str, HexBitwiseIterator("EE00D40C823060"))) == "11101110000000001101010000001100100000100011000001100000"
    #
    #
    # get_sum("EE00D40C823060")
    # get_sum("38006F45291200")
    # assert get_sum("8A004A801A8002F478") == 16
    # assert get_sum("620080001611562C8802118E34") == 12
    # assert get_sum("C0015000016115A2E0802F182340") == 23
    # assert get_sum("A0016C880162017C3686B18A3D4780") == 31
    print(get_sum(INPUT))
