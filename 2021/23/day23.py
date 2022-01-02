import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable, Optional

CORRECT_ROOMS = ['A','B','C','D']


@dataclass(frozen=True, order=True)
class Amphipod:
    color: str = field(compare=True)
    starting_room: int = field(compare=True)
    pos: int = field(compare=True)  # 0 is top

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

    def __len__(self):
        return len(self.members)

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
    depth: int,
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
                    depth - len(new_room) + 1
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
                        depth,
                    ))

            else:
                # to the left
                new_room: Room = rooms[move.amphipod.starting_room].remove(move.amphipod.color)
                new_rooms = tuple(room if i != move.amphipod.starting_room else new_room for i, room in enumerate(rooms))
                right = move.amphipod.starting_room + 1
                for steps, i in enumerate(range(right, -1, -1)):
                    new_hallway = list(hallway)
                    if hallway[i]:
                        break
                    new_hallway[i] = move.amphipod
                    steps_taken = get_hallway_real_distance(i, right) + 1 + (
                        move.amphipod.pos + 1
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
                            depth,
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
                        move.amphipod.pos + 1
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
                            depth,
                        )
                    )

    cache[cache_key] = min_energy
    return min_energy


def get_min_energy(config: list[tuple[str, ...]]) -> int:
    """

    :param config: starting config starting from the left, where each tuple is top to bottom
    :return: all possible moves
    """
    amphipods_by_room: dict[int, tuple[Amphipod, ...]] = {}
    for room, pods in enumerate(config):
        room_list = []
        for i, color in enumerate(pods):
            amphipod = Amphipod(color=color, starting_room=room, pos=i)
            room_list.append(amphipod)
        amphipods_by_room[room] = tuple(room_list)

    depth = len(amphipods_by_room[0])

    moves_by_amphipod = defaultdict(dict)
    for top_to_bottom in amphipods_by_room.values():
        last_out_rule = None
        for i, amphipod in enumerate(top_to_bottom):
            dependencies = frozenset({last_out_rule}) if last_out_rule else frozenset()
            rule = Move(amphipod=amphipod, type="out", dependencies=dependencies)
            moves_by_amphipod[amphipod]["out"] = rule
            last_out_rule = rule

    for amphipod in moves_by_amphipod:
        dependencies = {
            moves_by_amphipod[amphipod]["out"]
        }
        dest_room = amphipod.dest()
        if amphipod.starting_room == dest_room:
            if amphipod.pos < depth - 1:  # if any below
                # find lowest one that's not in the right room
                pods_below = [pod for pod in amphipods_by_room[dest_room] if pod.dest() != dest_room and pod.pos > amphipod.pos]
                if pods_below:
                    lowest = max(pods_below, key=lambda pod: pod.pos)
                    dependencies.add(moves_by_amphipod[lowest]["out"])
                    dest_move = Move(amphipod=amphipod, type="dest", dependencies=frozenset(dependencies))
                    moves_by_amphipod[amphipod]["dest"] = dest_move
            else:
                # none are below and we're already in the right room
                del moves_by_amphipod[amphipod]["out"]
        else:
            pods_not_in_right_room = [pod for pod in amphipods_by_room[dest_room] if pod.dest() != dest_room]
            if pods_not_in_right_room:
                lowest = max(pods_not_in_right_room, key=lambda pod: pod.pos)
                dependencies.add(moves_by_amphipod[lowest]["out"])
            dest_move = Move(amphipod=amphipod, type="dest", dependencies=frozenset(dependencies))
            moves_by_amphipod[amphipod]["dest"] = dest_move

    all_moves = set()
    for moves_by_type in moves_by_amphipod.values():
        for move in moves_by_type.values():
            all_moves.add(move)

    rooms = tuple(
        Room(t) for t in config
    )

    all_possible_orders = get_possible_move_orders(all_moves, [], [None for _ in range(7)], {}, rooms, depth)
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
    # get_min_energy([("B","D", "D", "A"), ("C", "C", "B", "D"), ("B", "B", "A", "C"), ("D", "A", "C", "A")])
    get_min_energy([("D", "D", "D","B"), ("D", "C", "B","A"), ("C", "B", "A","B"), ("C", "A", "C","A")])
    end = time.perf_counter()
    print(end - start)

    # 16089 too high
