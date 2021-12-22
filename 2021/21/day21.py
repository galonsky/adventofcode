from abc import ABC
from functools import reduce, cache


class DieValueProvider(ABC):
    def get_value(self) -> int:
        raise NotImplementedError


class DeterministicValueProvider(DieValueProvider):
    def __init__(self):
        self.next_val = 1

    def get_value(self) -> int:
        ret = self.next_val
        self.next_val += 1
        if self.next_val == 101:
            self.next_val = 1
        return ret


class Die:
    def __init__(self, value_provider: DieValueProvider):
        self.times_rolled = 0
        self.value_provider = value_provider

    def roll(self) -> int:
        self.times_rolled += 1
        return self.value_provider.get_value()


def get_new_position(starting_pos: int, delta: int) -> int:
    new_position = (starting_pos + delta) % 10
    if new_position == 0:
        new_position = 10
    return new_position


def play_game(positions: list[int]) -> int:
    scores = [0 for _ in positions]
    die = Die(DeterministicValueProvider())

    while True:
        for player, position in enumerate(positions):
            total_dice_roll = sum(die.roll() for _ in range(3))
            new_position = (position + total_dice_roll) % 10
            if new_position == 0:
                new_position = 10
            positions[player] = new_position
            scores[player] += new_position
            if scores[player] >= 1000:
                loser_score = scores[0] if player == 1 else scores[1]
                return loser_score * die.times_rolled


@cache
def num_wins(p1pos: int, p2pos: int, p1score: int, p2score: int) -> tuple[int, int]:
    if p1score >= 21:
        return (1, 0)
    if p2score >= 21:
        return (0, 1)

    totals = (0, 0)
    for d1 in range(1, 4):
        for d2 in range(1, 4):
            for d3 in range(1, 4):
                p1_newpos = get_new_position(p1pos, d1 + d2 + d3)
                p1newscore = p1score + p1_newpos

                # Switching the arguments here alternates whose turn it is
                p1_unis, p2_unis = num_wins(p2pos, p1_newpos, p2score, p1newscore)
                totals = (totals[0] + p2_unis, totals[1] + p1_unis)
    return totals


if __name__ == '__main__':
    print(num_wins(3, 10, 0, 0))
