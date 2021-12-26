import time
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import permutations
from typing import Iterable, Optional

CORRECT_ROOMS = ['A','B','C','D']


@dataclass(frozen=True)
class Amphipod:
    color: str
    starting_room: int
    top: bool

    def dest(self) -> int:
        return CORRECT_ROOMS.index(self.color)

    def get_energy_per_move(self) -> int:
        return pow(10, (ord(self.color) - ord('A')))


@dataclass(frozen=True, unsafe_hash=True)
class Move:
    amphipod: Amphipod
    type: str
    dependencies: frozenset["Move"] = field(compare=False)


def get_hallway_real_distance(left: int, right: int) -> int:
    dist_in_middle = (min(right, 5) - max(left, 1)) * 2
    if left == 0:
        dist_in_middle += 1
    if right == 6:
        dist_in_middle += 1
    return dist_in_middle


"""
#############
#01.2.3.4.56#
###B#C#B#D###
  #A#D#C#A#
  #########
"""


def get_possible_move_orders(
    moves_left: set[Move],
    already_done: list[Move],
    hallway: list[Optional[Amphipod]],
    cache: dict[tuple[frozenset[Move], tuple[Optional[Amphipod]]], int],
    energy_so_far: int = 0,
) -> int:
    already_done_set = frozenset(already_done)
    cache_key = (frozenset(moves_left), tuple(hallway))
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    if not moves_left:
        return energy_so_far
    min_energy = float('inf')
    for move in moves_left:
        if move.dependencies <= already_done_set:
            new_hallway = list(hallway)
            if move.type == "dest":
                # dest + 1 is the spot to the left of the room
                hallway_idx = hallway.index(move.amphipod)
                dest = move.amphipod.dest()
                if dest + 1 >= hallway_idx:
                    # dest is to the right
                    left = hallway_idx
                    right = dest + 1
                    hallway_to_traverse = hallway[left+1:right+1]
                    if hallway_to_traverse and any(hallway_to_traverse):
                        continue
                else:
                    # dest is to the left
                    left = dest + 2
                    right = hallway_idx
                    hallway_to_traverse = hallway[left:right]
                    if hallway_to_traverse and any(hallway_to_traverse):
                        continue
                new_hallway[hallway_idx] = None
                steps_taken = get_hallway_real_distance(left, right) + 1 + (
                    1 if (
                        [m for m in already_done if m.amphipod.color == move.amphipod.color and m.type == "dest"]
                        or len([m for m in already_done_set | moves_left if m.amphipod.color == move.amphipod.color and m.type == "dest"]) < 2
                    )
                    else 2
                )
                energy = steps_taken * move.amphipod.get_energy_per_move()
                min_energy = min(min_energy, get_possible_move_orders(moves_left - {move}, already_done + [move], new_hallway, cache, energy_so_far + energy))
            else:
                # to the left

                right = move.amphipod.starting_room + 1
                for steps, i in enumerate(range(right, -1, -1)):
                    new_hallway = list(hallway)
                    if hallway[i] or steps > 1:
                        break
                    new_hallway[i] = move.amphipod
                    steps_taken = get_hallway_real_distance(i, right) + 1 + (
                        1 if move.amphipod.top
                        else 2
                    )
                    energy = steps_taken * move.amphipod.get_energy_per_move()
                    min_energy = min(min_energy, get_possible_move_orders(moves_left - {move}, already_done + [move], new_hallway, cache, energy_so_far + energy))
                # to the right

                left = move.amphipod.starting_room + 2
                for steps, i in enumerate(range(left, len(hallway))):
                    new_hallway = list(hallway)
                    if hallway[i] or steps > 1:
                        break
                    new_hallway[i] = move.amphipod
                    steps_taken = get_hallway_real_distance(left, i) + 1 + (
                        1 if move.amphipod.top
                        else 2
                    )
                    energy = steps_taken * move.amphipod.get_energy_per_move()
                    min_energy = min(min_energy, get_possible_move_orders(moves_left - {move}, already_done + [move], new_hallway, cache, energy_so_far + energy))

    # cache[cache_key] = min_energy
    return min_energy


def get_min_energy(config: list[tuple[str, str]]) -> int:
    """

    :param config: starting config starting from the left, where each tuple is (top, bottom)
    :return: all possible moves
    """
    amphipods_by_room: dict[int, tuple[Amphipod, Amphipod]] = {}
    for i, (top, bottom) in enumerate(config):
        top = Amphipod(color=top, starting_room=i, top=True)
        bottom = Amphipod(color=bottom, starting_room=i, top=False)
        amphipods_by_room[i] = top, bottom

    moves_by_amphipod = defaultdict(dict)
    for top, bottom in amphipods_by_room.values():
        top_out = Move(amphipod=top, type="out", dependencies=frozenset())
        moves_by_amphipod[top]["out"] = top_out
        bottom_out = Move(amphipod=bottom, type="out", dependencies=frozenset({top_out}))
        moves_by_amphipod[bottom]["out"] = bottom_out

    for amphipod in moves_by_amphipod:
        dependencies = {
            moves_by_amphipod[amphipod]["out"]
        }
        dest_room = amphipod.dest()
        if amphipod.starting_room == dest_room:
            if amphipod.top:
                bottom = amphipods_by_room[dest_room][1]
                if bottom.dest() != dest_room:
                    dependencies.add(moves_by_amphipod[bottom]["out"])
                    dest_move = Move(amphipod=amphipod, type="dest", dependencies=frozenset(dependencies))
                    moves_by_amphipod[amphipod]["dest"] = dest_move
            else:
                del moves_by_amphipod[amphipod]["out"]
            continue


        dest_top, dest_bottom = amphipods_by_room[dest_room]
        if dest_bottom.color != CORRECT_ROOMS[dest_room]:
            dependencies.add(moves_by_amphipod[dest_bottom]["out"])
        if dest_top.color != CORRECT_ROOMS[dest_room]:
            dependencies.add(moves_by_amphipod[dest_top]["out"])
        dest_move = Move(amphipod=amphipod, type="dest", dependencies=frozenset(dependencies))
        moves_by_amphipod[amphipod]["dest"] = dest_move

    all_moves = set()
    for moves_by_type in moves_by_amphipod.values():
        for move in moves_by_type.values():
            all_moves.add(move)

    all_possible_orders = get_possible_move_orders(all_moves, [], [None for _ in range(7)], {})
    print(all_possible_orders)
    # print(len(all_possible_orders))
    # simplified = []
    # for order in all_possible_orders:
    #     simplified.append("".join(move.amphipod.color for move in order))
    #
    # for order in sorted(simplified):
    #     print(order)
    # print(len(all_possible_orders))


if __name__ == '__main__':
    start = time.perf_counter()
    get_min_energy([("B","A"), ("C", "D"), ("B", "C"), ("D", "A")])
    end = time.perf_counter()
    print(end - start)
