import re
from dataclasses import dataclass
from typing import Iterable, Tuple

LINE_PATTERN = re.compile(r'(\d+)-(\d+) ([a-z]): ([a-z]+)')


@dataclass
class PasswordRule:
    min_letters: int
    max_letters: int
    letter: str

    def validate(self, password: str) -> bool:
        return self.min_letters <= password.count(self.letter) <= self.max_letters


def get_input(filename: str) -> Iterable[str]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip()


def parse_line(line: str) -> Tuple[PasswordRule, str]:
    match = LINE_PATTERN.match(line)
    return (
        PasswordRule(min_letters=int(match.group(1)), max_letters=int(match.group(2)), letter=match.group(3)),
        match.group(4),
    )


if __name__ == '__main__':
    input = get_input('input.txt')
    num_valid = 0
    for line in input:
        rule, password = parse_line(line)
        # print(rule, password)
        if rule.validate(password):
            num_valid += 1
    print(num_valid)
