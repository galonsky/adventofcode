import re
from typing import Generator, Iterable


NUMBERS = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine"
]

DIGIT_PATTERN = '|'.join(['\\d'] + NUMBERS)
REVERSE_DIGIT_PATTERN = '|'.join(['\\d'] + [''.join(reversed(num)) for num in NUMBERS])


def get_input(filename: str) -> Generator[str, None, None]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()


def get_sum_of_calibration_values(lines: Iterable[str]) -> int:
    total = 0
    for line in lines:
        matches = re.findall(r'\d', line)
        value_str = matches[0] + matches[-1]
        total += int(value_str)
    return total


def _parse_digit(digit: str) -> str:
    if digit.isnumeric():
        return digit
    try:
        index = NUMBERS.index(digit)
    except ValueError:
        index = NUMBERS.index(''.join(reversed(digit)))
    if index < 0:
        raise Exception('not found!')
    return str(index + 1)


def get_sum_of_calibration_values_with_words(lines: Iterable[str]) -> int:
    total = 0
    for line in lines:
        first_match = re.search(DIGIT_PATTERN, line)
        last_match = re.search(REVERSE_DIGIT_PATTERN, ''.join(reversed(line)))
        value_str = _parse_digit(first_match.group()) + _parse_digit(last_match.group() if last_match else first_match.group())
        print(f"{line},{value_str}")
        total += int(value_str)
    return total


if __name__ == '__main__':
    input = list(get_input("input.txt"))
    # print(get_sum_of_calibration_values(input))
    print(get_sum_of_calibration_values_with_words(input))
