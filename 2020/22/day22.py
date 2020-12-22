from collections import deque
from itertools import islice
from typing import Iterable, Deque, List, Callable


def get_decks(filename: str) -> Iterable[Deque[int]]:
    with open(filename, 'r') as file:
        contents = file.read()
        players = contents.split('\n\n')
        for player in players:
            yield deque(map(int, player.split('\n')[1:]))


def get_history_key(decks: List[Deque[int]]) -> str:
    return ','.join(map(str, decks[0])) + '|' + ','.join(map(str, decks[0]))


def play_game(decks: List[Deque[int]]) -> int:
    while all(len(deck) > 0 for deck in decks):
        player1_card = decks[0].popleft()
        player2_card = decks[1].popleft()
        if player1_card > player2_card:
            decks[0].append(player1_card)
            decks[0].append(player2_card)
        elif player2_card > player1_card:
            decks[1].append(player2_card)
            decks[1].append(player1_card)
    return 0 if len(decks[1]) == 0 else 1


def play_recursive_game(decks: List[Deque[int]]) -> int:
    round_history = set()
    while all(len(deck) > 0 for deck in decks):
        history_key = get_history_key(decks)
        if history_key in round_history:
            return 0
        round_history.add(history_key)

        player1_card = decks[0].popleft()
        player2_card = decks[1].popleft()
        if len(decks[0]) >= player1_card and len(decks[1]) >= player2_card:
            player1_copy = deque(islice(decks[0], player1_card))
            player2_copy = deque(islice(decks[1], player2_card))
            winner = play_recursive_game([player1_copy, player2_copy])
        else:
            winner = 0 if player1_card > player2_card else 1

        if winner == 0:
            decks[0].append(player1_card)
            decks[0].append(player2_card)
        else:
            decks[1].append(player2_card)
            decks[1].append(player1_card)
    return 0 if len(decks[1]) == 0 else 1


def part1():
    decks = list(get_decks('input.txt'))

    winner_index = play_game(decks)
    winner_deck = decks[winner_index]
    score = 0
    multiplier = 1
    for card in reversed(winner_deck):
        score += card * multiplier
        multiplier += 1
    return score


def part2():
    decks = list(get_decks('input.txt'))

    winner_index = play_recursive_game(decks)
    winner_deck = decks[winner_index]
    score = 0
    multiplier = 1
    for card in reversed(winner_deck):
        score += card * multiplier
        multiplier += 1
    return score



if __name__ == '__main__':
    print(part2())