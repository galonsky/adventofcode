import re


MARKER_PATTERN = re.compile(r'\((\d+)x(\d+)\)')


def decompress(compressed: str) -> str:
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


def get_decompressed_length(compressed: str) -> int:
    match = MARKER_PATTERN.search(compressed)
    if not match:
        return len(compressed)

    pattern_len = int(match.group(1))
    repetitions = int(match.group(2))
    pattern = compressed[match.end():match.end() + pattern_len]

    return (
        match.start()  # everything before the marker
        + repetitions * get_decompressed_length(pattern)
        + get_decompressed_length(compressed[match.end()+pattern_len:])
    )

def part1():
    # print(decompress('ADVENT'))
    # print(decompress('A(1x5)BC'))
    # print(decompress('(3x3)XYZ'))
    # print(decompress('A(2x2)BCD(2x2)EFG'))
    # print(decompress('(6x1)(1x3)A'))
    # print(decompress('X(8x2)(3x3)ABCY'))
    decompressed = decompress(open('input.txt').read())
    print(len(decompressed))


def part2():
    # print(get_decompressed_length('(3x3)XYZ'))
    # print(get_decompressed_length('X(8x2)(3x3)ABCY'))
    # print(get_decompressed_length('(27x12)(20x12)(13x14)(7x10)(1x12)A'))
    # print(get_decompressed_length('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'))
    print(get_decompressed_length(open('input.txt').read()))



if __name__ == '__main__':
    part2()
