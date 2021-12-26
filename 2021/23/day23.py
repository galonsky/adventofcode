import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import permutations
from typing import Iterable, Optional

CORRECT_ROOMS = ['A','B','C','D']


@dataclass(frozen=True, order=True)
class Amphipod:
    color: str = field(compare=True)
    starting_room: int = field(compare=True)
    top: bool = field(compare=True)

    def dest(self) -> int:
        return CORRECT_ROOMS.index(self.color)

    def get_energy_per_move(self) -> int:
        return pow(10, (ord(self.color) - ord('A')))


@dataclass(frozen=True, unsafe_hash=True, order=True)
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


class Room:
    def __init__(self, members: Iterable[str]):
        self.members = list(members)

    def __hash__(self) -> int:
        return hash(json.dumps(self.members))

    def __eq__(self, other):
        return self.members == other.members

    def add(self, other: str):
        return Room(self.members + [other])

    def remove(self, other: str):
        new_list = list(self.members)
        new_list.remove(other)
        return Room(new_list)


@dataclass(frozen=True)
class BoardState:
    # moves_left: frozenset[Move]
    hallway: tuple[Optional[Amphipod]]
    rooms: tuple[Room]


def get_possible_move_orders(
    moves_left: set[Move],
    already_done: list[Move],
    hallway: list[Optional[Amphipod]],
    cache: dict[BoardState, int],
    rooms: tuple[Room],
) -> int:
    already_done_set = frozenset(already_done)
    cache_key = BoardState(
        # moves_left=frozenset(moves_left),
        hallway=tuple(hallway),
        rooms=rooms,
    )
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    if not moves_left:
        return 0
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
                new_room = rooms[dest].add(move.amphipod.color)
                new_rooms = tuple(room if i != dest else new_room for i, room in enumerate(rooms))
                new_hallway[hallway_idx] = None
                steps_taken = get_hallway_real_distance(left, right) + 1 + (
                    1 if (
                        [m for m in already_done if m.amphipod.color == move.amphipod.color and m.type == "dest"]
                        or len([m for m in already_done_set | moves_left if m.amphipod.color == move.amphipod.color and m.type == "dest"]) < 2
                    )
                    else 2
                )
                energy = steps_taken * move.amphipod.get_energy_per_move()
                min_energy = min(
                    min_energy,
                    energy + get_possible_move_orders(
                        moves_left - {move},
                        already_done + [move],
                        new_hallway,
                        cache,
                        new_rooms,
                    ))

            else:
                # to the left
                new_room = rooms[move.amphipod.starting_room].remove(move.amphipod.color)
                new_rooms = tuple(room if i != move.amphipod.starting_room else new_room for i, room in enumerate(rooms))
                right = move.amphipod.starting_room + 1
                for steps, i in enumerate(range(right, -1, -1)):
                    new_hallway = list(hallway)
                    if hallway[i]:
                        break
                    new_hallway[i] = move.amphipod
                    steps_taken = get_hallway_real_distance(i, right) + 1 + (
                        1 if move.amphipod.top
                        else 2
                    )
                    energy = steps_taken * move.amphipod.get_energy_per_move()
                    min_energy = min(
                        min_energy,
                        energy + get_possible_move_orders(
                            moves_left - {move},
                            already_done + [move],
                            new_hallway,
                            cache,
                            new_rooms,
                        )
                    )
                # to the right

                left = move.amphipod.starting_room + 2
                for steps, i in enumerate(range(left, len(hallway))):
                    new_hallway = list(hallway)
                    if hallway[i]:
                        break
                    new_hallway[i] = move.amphipod
                    steps_taken = get_hallway_real_distance(left, i) + 1 + (
                        1 if move.amphipod.top
                        else 2
                    )
                    energy = steps_taken * move.amphipod.get_energy_per_move()
                    min_energy = min(
                        min_energy,
                        energy + get_possible_move_orders(
                            moves_left - {move},
                            already_done + [move],
                            new_hallway,
                            cache,
                            new_rooms,
                        )
                    )

    cache[cache_key] = min_energy
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

    rooms = tuple(
        Room(t) for t in config
    )

    all_possible_orders = get_possible_move_orders(all_moves, [], [None for _ in range(7)], {}, rooms)
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
    # get_min_energy([("D", "B"), ("D", "A"), ("C", "B"), ("C", "A")])
    end = time.perf_counter()
    print(end - start)

    # 16089 too high
