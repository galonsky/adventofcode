from abc import ABC


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


if __name__ == '__main__':
    # for i in range(1, 100):
    #     print(i % 10 )
    print(play_game([3, 10]))