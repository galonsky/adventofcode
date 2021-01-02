import re
from functools import reduce
from typing import Iterable, Set

BRACKET_PATTERN = re.compile(r'\[([a-z]+)]')


def has_abba(string: str) -> bool:
    if len(string) < 4:
        return False
    for i in range(len(string) - 3):
        if string[i] == string[i+1]:
            continue
        if string[i+2] == string[i+1] and string[i+3] == string[i]:
            return True
    return False


def get_babs(string: str) -> Set[str]:
    babs = set()
    if len(string) < 3:
        return babs
    for i in range(len(string) - 2):
        if string[i] == string[i+1]:
            continue
        if string[i] == string[i+2]:
            babs.add(string[i:i+3])
    return babs


def supports_tls(string: str) -> bool:
    bracket_matches = BRACKET_PATTERN.finditer(string)
    for match in bracket_matches:
        if has_abba(match.group(1)):
            return False
    non_bracket_strings = BRACKET_PATTERN.split(string)[0::2]  # skipping every other since it's including capturing group
    for string in non_bracket_strings:
        if has_abba(string):
            return True
    return False


def get_opposite(string: str) -> str:
    return string[1] + string[0] + string[1]


def supports_ssl(string: str) -> bool:
    bracket_matches = BRACKET_PATTERN.finditer(string)
    all_babs = reduce(lambda s1, s2: s1 | s2, [get_babs(match.group(1)) for match in bracket_matches])
    non_bracket_strings = BRACKET_PATTERN.split(string)[0::2]  # skipping every other since it's including capturing group
    all_abas = reduce(lambda s1, s2: s1 | s2, [get_babs(string) for string in non_bracket_strings])
    for aba in all_abas:
        if get_opposite(aba) in all_babs:
            return True
    return False


def get_input(filename: str) -> Iterable[str]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip('\n')


def part1():
    # print(supports_tls('abba[mnop]qrst'))
    # print(supports_tls('abcd[bddb]xyyx'))
    # print(supports_tls('aaaa[qwer]tyui'))
    # print(supports_tls('ioxxoj[asdfgh]zxcvbn'))
    num_tls = 0
    for string in get_input('input.txt'):
        if supports_tls(string):
            num_tls += 1
    print(num_tls)


def part2():
    # print(supports_ssl('aba[bab]xyz'))
    # print(supports_ssl('xyx[xyx]xyx'))
    # print(supports_ssl('aaa[kek]eke'))
    # print(supports_ssl('zazbz[bzb]cdb'))

    num_ssl = 0
    for string in get_input('input.txt'):
        if supports_ssl(string):
            num_ssl += 1
    print(num_ssl)


if __name__ == '__main__':
    part2()
