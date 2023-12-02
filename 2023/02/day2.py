import re
import dataclasses
from collections import defaultdict

LINE_PATTERN = re.compile(r'Game (\d+): (.+)')
COLOR_GROUP_PATTERN = re.compile(r'(\d+) (.+)')


def get_input(filename: str) -> dict[int, list[dict[str, int]]]:
    groups = defaultdict(list)
    with open(filename, 'r') as file:
        for line in file:
            line_match = LINE_PATTERN.match(line.strip())
            game_id = int(line_match.group(1))
            handfuls = line_match.group(2).split("; ")
            handfuls_list = []
            for handful in handfuls:
                handful_dict = {}
                for group_str in handful.split(', '):
                    group_match = COLOR_GROUP_PATTERN.match(group_str)
                    handful_dict[group_match.group(2)] = int(group_match.group(1))
                handfuls_list.append(handful_dict)
            groups[game_id] = handfuls_list
    return groups


def is_group_possible(color_group: dict[str, int]) -> bool:
    return color_group.get("red", 0) <= 12 and color_group.get("green", 0) <= 13 and color_group.get("blue", 0) <= 14


def get_sum_possible_games(games: dict[int, list[dict[str, int]]]) -> int:
    total = 0
    for game_id, handfuls in games.items():
        if all(is_group_possible(group) for group in handfuls):
            total += game_id
    return total


def get_sum_of_power(games: dict[int, list[dict[str, int]]]) -> int:
    total = 0
    for game_id, handfuls in games.items():
        max_red = max(handful.get("red", 0) for handful in handfuls)
        max_green = max(handful.get("green", 0) for handful in handfuls)
        max_blue = max(handful.get("blue", 0) for handful in handfuls)
        total += max_red * max_green * max_blue
    return total


if __name__ == '__main__':
    games = get_input("input.txt")
    print(get_sum_possible_games(games))
    print(get_sum_of_power(games))