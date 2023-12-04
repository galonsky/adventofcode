import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Generator, Iterable

CARD_PATTERN = re.compile(r'Card\s+(\d+):([0-9 ]+)\|([0-9 ]+)')


@dataclass
class Card:
    id: int
    winning_nums: set[int]
    your_nums: set[int]

    def score(self) -> int:
        num_winners = self.num_winners()
        if not num_winners:
            return 0
        return 2 ** (num_winners - 1)

    def num_winners(self):
        return len(self.winning_nums & self.your_nums)


def _nums_to_set(nums: str) -> set[int]:
    return set(int(num) for num in nums.split())


def get_cards(filename: str) -> Generator[Card, None, None]:
    with open(filename, 'r') as file:
        for line in file:
            match = CARD_PATTERN.match(line.strip())
            yield Card(id=int(match.group(1)), winning_nums=_nums_to_set(match.group(2)), your_nums=_nums_to_set(match.group(3)))


def get_total_score(cards: Iterable[Card]) -> int:
    total = 0
    for card in cards:
        total += card.score()
    return total


def get_num_cards(cards: Iterable[Card]) -> int:
    num_per_card_id = {
        card.id: 1
        for card in cards
    }
    for card in cards:
        num_winners = card.num_winners()
        for i in range(card.id + 1, card.id + 1 + num_winners):
            num_per_card_id[i] += num_per_card_id[card.id]
    return sum(num_per_card_id.values())


if __name__ == '__main__':
    cards = list(get_cards("input.txt"))
    print(get_num_cards(cards))