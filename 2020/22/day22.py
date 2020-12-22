from collections import deque
from typing import Iterable, Deque


def get_decks(filename: str) -> Iterable[Deque[int]]:
    with open(filename, 'r') as file:
        contents = file.read()
        players = contents.split('\n\n')
        for player in players:
            yield deque(map(int, player.split('\n')[1:]))


def part1():
    decks = list(get_decks('input.txt'))
    while all(len(deck) > 0 for deck in decks):
        player1_card = decks[0].popleft()
        player2_card = decks[1].popleft()

        if player1_card > player2_card:
            decks[0].append(player1_card)
            decks[0].append(player2_card)
        elif player2_card > player1_card:
            decks[1].append(player2_card)
            decks[1].append(player1_card)
        else:
            raise Exception('undefined?')

    winner_deck = decks[0] if len(decks[1]) == 0 else decks[1]
    score = 0
    multiplier = 1
    for card in reversed(winner_deck):
        score += card * multiplier
        multiplier += 1
    return score



if __name__ == '__main__':
    print(part1())