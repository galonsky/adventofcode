from collections import deque
from typing import Deque, List, Optional, Iterable


def factory_order_deck(num_cards: int) -> Deque[int]:
    deck = deque()
    for i in range(num_cards):
        # top of the deck is left side
        deck.append(i)
    return deck


def deal_into_new_stack(deck: Deque[int]) -> Deque[int]:
    deck.reverse()
    return deck


def cut(deck: Deque[int], n: int) -> Deque[int]:
    deck.rotate(-n)
    return deck


def deal_with_increment(deck: Deque[int], n: int) -> Deque[int]:
    new_list: List[Optional[int]] = [None] * len(deck)
    i = 0
    for card in deck:
        new_list[i % len(deck)] = card
        i += n
    return deque(new_list)


def get_instructions(filename: str) -> Iterable[str]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip('\n')


def part1():
    # print(deal_into_new_stack(factory_order_deck(10)))
    # print(cut(factory_order_deck(10), 3))
    # print(cut(factory_order_deck(10), -4))
    # print(deal_with_increment(factory_order_deck(10), 3))
    deck = factory_order_deck(10007)
    for instruction in get_instructions('input.txt'):
        if instruction == 'deal into new stack':
            deck = deal_into_new_stack(deck)
        elif instruction.startswith('deal with increment'):
            increment = int(instruction.split('deal with increment ')[1])
            deck = deal_with_increment(deck, increment)
        else:
            n = int(instruction.split('cut ')[1])
            deck = cut(deck, n)

    for i, card in enumerate(deck):
        if card == 2019:
            return i





if __name__ == '__main__':
    print(part1())

