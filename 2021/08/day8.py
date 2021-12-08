from collections import defaultdict
from copy import deepcopy
from typing import Iterable


def get_data(filename: str) -> list[tuple[list[str], list[str]]]:
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            left, right = tuple(line.split("|"))
            lines.append((left.split(), right.split()))
    return lines


UNIQUE_LENGTHS = {2, 3, 4, 7}


POSSIBILITIES_BY_NUM_SEGMENTS = {
    2: {1},
    3: {7},
    4: {4},
    5: {2, 3, 5},
    6: {0, 9, 6},
    7: {8},
}

LETTERS_USED_BY_DIGITS = {
    0: set("abcefg"),
    1: set("cf"),
    2: set("acdeg"),
    3: set("acdfg"),
    4: set("bcdf"),
    5: set("abdfg"),
    6: set("abdefg"),
    7: set("acf"),
    8: set("abcdefg"),
    9: set("abcdfg"),
}

DIGITS_BY_SEGMENTS = {frozenset(v): k for k, v in LETTERS_USED_BY_DIGITS.items()}


# If we have situations where there is one instance of one possibility, two instance of two possibilities,
# these characters can't be in the other possibilities
def reduce_possibilities(possibilities: dict[str, set[str]]) -> None:
    unique_set_counts = defaultdict(int)
    for poss_set in possibilities.values():
        unique_set_counts[frozenset(poss_set)] += 1

    for unique_set, count in unique_set_counts.items():
        if len(unique_set) != count:
            continue

        for ch, existing_poss in possibilities.items():
            if unique_set < existing_poss:
                possibilities[ch] = existing_poss - unique_set


# Returns all possible decoder dicts (single char to single char)
def get_all_possibility_dicts(possibilities: dict[str, set[str]]) -> Iterable[dict[str, str]]:
    if max(len(poss) for poss in possibilities.values()) == 1:
        yield {ch: next(iter(poss)) for ch, poss in possibilities.items()}
    for ch, poss in possibilities.items():
        if len(possibilities[ch]) == 1:
            continue
        for poss_char in possibilities[ch]:
            new_dict = deepcopy(possibilities)
            new_dict[ch] = {poss_char}
            reduce_possibilities(new_dict)
            yield from get_all_possibility_dicts(new_dict)
        return


def possibility_works_for_signals(poss: dict[str, str], signals: list[str]) -> bool:
    for signal in signals:
        segments = set(poss[ch] for ch in signal)
        if segments not in LETTERS_USED_BY_DIGITS.values():
            return False
    return True


def generate_decoded_number(decoder: dict[str, str], digits: list[str]) -> int:
    num_str = ""
    for digit in digits:
        segments = frozenset(decoder[ch] for ch in digit)
        num_str += str(DIGITS_BY_SEGMENTS[segments])
    return int(num_str)


def decode(signal_patterns: list[str], output_digits: list[str]) -> int:
    possibilities = {i: set("abcdefg") for i in "abcdefg"}

    # Start with patterns with unique lengths and reduce
    for length, poss_digits in POSSIBILITIES_BY_NUM_SEGMENTS.items():
        if len(poss_digits) != 1:
            continue
        digit = next(iter(poss_digits))
        letters_used = LETTERS_USED_BY_DIGITS[digit]
        pattern = next(iter(pat for pat in signal_patterns if len(pat) == length))
        for ch in pattern:
            possibilities[ch] &= letters_used

    # By observation, doing this always gets down to 2
    while max(len(poss) for poss in possibilities.values()) > 2:
        reduce_possibilities(possibilities)

    # This should only be 8 possibilities, 2^3
    all_possibilities = get_all_possibility_dicts(possibilities)
    working_possibilities = [poss for poss in all_possibilities if possibility_works_for_signals(poss, signal_patterns)]
    assert len(working_possibilities) == 1

    return generate_decoded_number(next(iter(working_possibilities)), output_digits)


def get_sum_of_decoded_values(data: list[tuple[list[str], list[str]]]) -> int:
    return sum(decode(left, right) for left, right in data)


def get_count_of_unique_digits(data: list[tuple[list[str], list[str]]]) -> int:
    count = 0
    for _, right in data:
        for digit in right:
            if len(digit) in UNIQUE_LENGTHS:
                count += 1
    return count


if __name__ == '__main__':
    print(get_sum_of_decoded_values(get_data("input.txt")))
