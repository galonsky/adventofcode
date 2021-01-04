import re


MARKER_PATTERN = re.compile(r'\((\d+)x(\d+)\)')


def decompress(compressed: str) -> str:
    match = MARKER_PATTERN.search(compressed)
    if not match:
        return compressed
    result = ''
    remaining = compressed
    while True:
        match = MARKER_PATTERN.search(remaining)
        if not match:
            result += remaining
            return result
        else:
            pattern_len = int(match.group(1))
            repetitions = int(match.group(2))

            # add everything before the marker
            result += remaining[:match.start()]
            pattern = remaining[match.end():match.end()+pattern_len]
            for _ in range(repetitions):
                result += pattern
            remaining = remaining[match.end()+pattern_len:]


def part1():
    # print(decompress('ADVENT'))
    # print(decompress('A(1x5)BC'))
    # print(decompress('(3x3)XYZ'))
    # print(decompress('A(2x2)BCD(2x2)EFG'))
    # print(decompress('(6x1)(1x3)A'))
    # print(decompress('X(8x2)(3x3)ABCY'))
    decompressed = decompress(open('input.txt').read())
    print(len(decompressed))


if __name__ == '__main__':
    part1()
